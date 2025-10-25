#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Converter API Blueprint
Handles conversion-related API endpoints
"""

from flask import Blueprint, request, jsonify, Response, current_app
import requests
import base64
import urllib.parse
import re
from web.blueprints.auth import login_required

converter_bp = Blueprint('converter', __name__)


@converter_bp.route('/api/parse/links', methods=['POST'])
@login_required
def parse_links():
    """Parse proxy links"""
    converter = current_app.config['CONVERTER']
    data = request.json
    links = data.get('links', [])

    nodes = []
    for link in links:
        proxy = converter.parse_link(link)
        if proxy:
            nodes.append(proxy)

    return jsonify({'nodes': nodes})


@converter_bp.route('/api/generate/config', methods=['POST'])
@login_required
def generate_config():
    """Generate configuration file"""
    converter = current_app.config['CONVERTER']
    data = request.json
    nodes = data.get('nodes', [])
    rule = data.get('rule', 'default')
    config_name = data.get('config_name', 'My Subscription Config')
    auto_update = data.get('auto_update', True)
    update_interval_hours = data.get('update_interval_hours', 24)
    traffic_limit_gb = data.get('traffic_limit_gb', 0)

    if not nodes:
        return jsonify({'error': 'No valid nodes'}), 400

    config = converter.generate_clash_config(nodes, rule)
    token = converter.save_conversion(config, len(nodes), config_name, auto_update,
                                      update_interval_hours, traffic_limit_gb)

    # Get request URL root (includes scheme, host, and base_path if configured)
    from flask import url_for
    # Use url_for to generate the correct URL with base_path
    url = url_for('converter.get_clash_config', token=token, _external=True)

    return jsonify({
        'success': True,
        'token': token,
        'url': url,
        'proxies_count': len(nodes),
        'auto_update': auto_update,
        'update_interval_hours': update_interval_hours,
        'traffic_limit_gb': traffic_limit_gb
    })


@converter_bp.route('/api/convert/links', methods=['POST'])
@login_required
def convert_links():
    """Convert proxy links"""
    converter = current_app.config['CONVERTER']
    data = request.json
    links = data.get('links', [])
    rule = data.get('rule', 'default')
    config_name = data.get('config_name', 'My Subscription Config')

    proxies = []
    for link in links:
        proxy = converter.parse_link(link)
        if proxy:
            proxies.append(proxy)

    if not proxies:
        return jsonify({'error': 'No valid proxy links'}), 400

    config = converter.generate_clash_config(proxies, rule)
    token = converter.save_conversion(config, len(proxies), config_name)

    # Get request URL root (includes scheme, host, and base_path if configured)
    from flask import url_for
    # Use url_for to generate the correct URL with base_path
    url = url_for('converter.get_clash_config', token=token, _external=True)

    return jsonify({
        'success': True,
        'token': token,
        'url': url,
        'proxies_count': len(proxies)
    })


@converter_bp.route('/api/convert/sub', methods=['GET'])
# @login_required  # Temporarily disabled for debugging
def convert_subscription():
    """Convert subscription links"""
    converter = current_app.config['CONVERTER']

    sub_url = request.args.get('url')
    rule = request.args.get('rule', 'default')
    config_name = request.args.get('config_name', 'Subscription Config')
    auto_update = request.args.get('auto_update', 'true').lower() == 'true'
    update_interval_hours = int(request.args.get('update_interval_hours', 24))
    traffic_limit_gb = int(request.args.get('traffic_limit_gb', 0))

    if not sub_url:
        return jsonify({'error': 'Missing subscription URL'}), 400

    try:
        # Fetch subscription content
        resp = requests.get(sub_url, timeout=10)
        content = resp.text

        # Try base64 decoding
        try:
            decoded = base64.b64decode(content).decode('utf-8')
            links = decoded.strip().split('\n')
        except:
            # If not base64, split by lines directly
            links = content.strip().split('\n')

        # Parse links
        proxies = []
        for link in links:
            proxy = converter.parse_link(link)
            if proxy:
                proxies.append(proxy)

        if not proxies:
            return jsonify({'error': 'No valid proxies in subscription'}), 400

        config = converter.generate_clash_config(proxies, rule)
        token = converter.save_conversion(config, len(proxies), config_name, auto_update,
                                          update_interval_hours, traffic_limit_gb)

        # Get request protocol and base_path
        scheme = 'https' if request.is_secure else 'http'
        base_path = current_app.config['APP_CONFIG']['server'].get('base_path', '')

        # Construct URL based on base_path
        if base_path:
            # Ensure it has slashes on both sides
            if not base_path.startswith('/'):
                base_path = '/' + base_path
            if not base_path.endswith('/'):
                base_path = base_path + '/'
            url = f"{scheme}://{request.host}{base_path}clash/{token}"
        else:
            # No base_path, use root
            url = f"{scheme}://{request.host}/clash/{token}"

        return jsonify({
            'success': True,
            'token': token,
            'url': url,
            'proxies_count': len(proxies),
            'auto_update': auto_update,
            'update_interval_hours': update_interval_hours,
            'traffic_limit_gb': traffic_limit_gb
        })

    except Exception as e:
        return jsonify({'error': f'Failed to fetch subscription: {str(e)}'}), 500


@converter_bp.route('/clash/<token>')
def get_clash_config(token):
    """Get Clash configuration with subscription settings"""
    converter = current_app.config['CONVERTER']

    try:
        config, config_name, auto_update, update_interval_hours, traffic_limit_gb = converter.get_conversion_with_settings(token)

        if not config:
            return jsonify({'error': 'Configuration not found'}), 404

        # Ensure filename doesn't contain .yaml suffix and is safe
        if config_name.endswith('.yaml') or config_name.endswith('.yml'):
            config_name = config_name.rsplit('.', 1)[0]

        # Process filename to support Chinese and other Unicode characters
        # Remove unsafe characters but preserve Chinese and other Unicode characters
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', config_name)

        # If filename is empty or only whitespace, use default name
        if not safe_name.strip():
            safe_name = f'clash_{token}'
        else:
            # Ensure filename is not too long (browser limitation)
            if len(safe_name.encode('utf-8')) > 200:
                safe_name = safe_name[:50] + f'_{token}'

        # Use RFC 6266 standard to support Unicode filenames
        # For Content-Disposition: filename should NOT include .yaml extension
        # because Clash clients use it for display purposes
        try:
            safe_name.encode('ascii')
            # For ASCII names, Clash Verge has issues with quoted filenames
            # Use RFC 5987 encoding for names with spaces to avoid quotes
            if ' ' in safe_name:
                # Use RFC 5987 encoding to avoid quotes (better for Clash Verge)
                encoded_name = urllib.parse.quote(safe_name)
                filename_header = f'inline; filename*=UTF-8\'\'{encoded_name}'
            elif '"' in safe_name or '\\' in safe_name:
                # Need quotes, escape any existing quotes
                escaped_name = safe_name.replace('\\', '\\\\').replace('"', '\\"')
                filename_header = f'inline; filename="{escaped_name}"'
            else:
                # No quotes needed for simple ASCII names (no spaces, no special chars)
                filename_header = f'inline; filename={safe_name}'
        except UnicodeEncodeError:
            # Contains non-ASCII characters, use RFC 5987 encoding
            # Some Clash clients may read the filename from Content-Disposition
            # So we keep it without .yaml extension for display purposes
            encoded_name_without_yaml = urllib.parse.quote(safe_name)
            filename_header = f'inline; filename*=UTF-8\'\'{encoded_name_without_yaml}'

        # URL-encode the profile title to handle Unicode characters (e.g., Chinese)
        # HTTP headers must be ASCII/Latin-1, so we encode Unicode as URL-encoded UTF-8
        # Note: profile-title should NOT include .yaml extension for display in Clash
        # Keep common ASCII characters unencoded for better readability
        encoded_title = urllib.parse.quote(safe_name, safe='-_.~')

        # Build subscription-userinfo header
        # When traffic_limit_gb is 0, Clash will show it as unlimited (∞)
        # We simply omit the subscription-userinfo header entirely when traffic is unlimited
        headers = {
            'Content-Type': 'text/yaml; charset=utf-8',
            'Content-Disposition': filename_header,
            'Cache-Control': 'no-cache',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'profile-title': encoded_title,  # Clash subscription display name without .yaml extension
        }

        # Only add profile-update-interval if auto-update is enabled
        if auto_update:
            headers['profile-update-interval'] = str(update_interval_hours)  # Auto-update interval in hours

        # Add subscription-userinfo header for traffic display in Clash clients
        # When traffic_limit_gb is 0, omit the header entirely - most clients show this as unlimited
        if traffic_limit_gb > 0:
            total_bytes = traffic_limit_gb * 1024 * 1024 * 1024
            # Don't include expire field to avoid date display issues in Clash Verge
            headers['subscription-userinfo'] = f'upload=0; download=0; total={total_bytes}'

        return Response(
            config,
            mimetype='text/yaml',
            headers=headers
        )
    except Exception as e:
        print(f"Error in get_clash_config: {e}")
        return jsonify({'error': 'Failed to get configuration'}), 500


@converter_bp.route('/api/history', methods=['GET'])
@login_required
def get_history():
    """Get history records"""
    converter = current_app.config['CONVERTER']
    return jsonify(converter.get_history())


@converter_bp.route('/api/history/<token>', methods=['DELETE'])
@login_required
def delete_history(token):
    """Delete history record"""
    converter = current_app.config['CONVERTER']
    converter.delete_conversion(token)
    return jsonify({'success': True})


@converter_bp.route('/api/history', methods=['DELETE'])
@login_required
def clear_history():
    """Clear history records"""
    converter = current_app.config['CONVERTER']
    converter.clear_all_history()
    return jsonify({'success': True})
