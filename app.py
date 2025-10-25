#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SubProtoX - VPN Subscription And Protocol Conversion Platform
Main application entry point (refactored)
"""

import os
import ssl
import argparse
import secrets
from flask import Flask

# Import configuration
try:
    from config import get_config
    CONFIG = get_config()
except ImportError:
    print("Warning: Configuration file config.py not found, using default configuration")
    CONFIG = {
        'server': {'host': '0.0.0.0', 'port': 7777, 'debug': False},
        'ssl': {'enabled': False, 'cert_path': '', 'key_path': ''},
        'database': {'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gringotts.db')},
        'rules': {'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rules')},
        'default_user': {'username': 'admin', 'password': 'admin'},
        'security': {'secret_key': None, 'session_timeout': 24 * 60 * 60},
        'converter': {'max_proxies': 1000, 'timeout': 30, 'user_agent': 'SubProtoX/1.0'},
        'log': {'level': 'INFO', 'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s', 'file': None},
        'github': {
            'enabled': True,
            'api_url': 'https://api.github.com',
            'repo_owner': 'maxiao0234',
            'repo_name': 'SubProtoX',
            'cache_duration': 3600,
            'timeout': 10
        }
    }

# Import core modules
from core.converter import SubConverter
from utils.github_api import GitHubAPI

# Import rules module
try:
    from rules import RuleManager
except ImportError:
    print("Warning: Rules module not found, using built-in rules")
    RuleManager = None

# Import blueprints
from web.blueprints import auth_bp, converter_bp, management_bp


def create_app(config=None):
    """Create and configure the Flask application"""
    app = Flask(__name__)

    # Use provided config or global CONFIG
    if config is None:
        config = CONFIG

    # Set secret key
    app.secret_key = config['security']['secret_key'] or secrets.token_hex(32)

    # Initialize SubConverter
    db_path = config['database']['path']
    rules_path = config['rules']['path']
    default_username = config['default_user']['username']
    default_password = config['default_user']['password']

    # Initialize rule manager
    rule_manager = None
    if RuleManager:
        rule_manager = RuleManager(db_path)

    # Create converter instance
    converter = SubConverter(
        db_path=db_path,
        rules_path=rules_path,
        default_username=default_username,
        default_password=default_password,
        rule_manager=rule_manager
    )

    # Initialize GitHub API
    github_api = None
    if config.get('github', {}).get('enabled'):
        github_api = GitHubAPI(config)

    # Store instances in app config for access in blueprints
    app.config['CONVERTER'] = converter
    app.config['GITHUB_API'] = github_api
    app.config['APP_CONFIG'] = config

    # Get base_path from config
    base_path = config['server'].get('base_path', '')

    # Normalize base_path: convert empty string to no prefix
    # If user inputs "subprotox", it becomes "/subprotox/"
    if base_path:
        # Ensure it starts and ends with /
        if not base_path.startswith('/'):
            base_path = '/' + base_path
        if not base_path.endswith('/'):
            base_path = base_path + '/'
        # Remove trailing slash for url_prefix (Flask requirement)
        url_prefix = base_path.rstrip('/')
    else:
        # Empty base_path means root path (no prefix)
        url_prefix = None

    # Register blueprints with url_prefix
    app.register_blueprint(auth_bp, url_prefix=url_prefix)
    app.register_blueprint(converter_bp, url_prefix=url_prefix)
    app.register_blueprint(management_bp, url_prefix=url_prefix)

    return app


def main():
    """Main function"""
    global CONFIG

    parser = argparse.ArgumentParser(description='VPN Subscription Converter Service')
    parser.add_argument('--port', type=int, default=CONFIG['server']['port'], help='Server port')
    parser.add_argument('--ssl', action='store_true', default=CONFIG.get('ssl', {}).get('enabled', False), help='Enable SSL')
    parser.add_argument('--host', default=CONFIG['server']['host'], help='Listen address')
    parser.add_argument('--config', default='config.py', help='Configuration file path')
    args = parser.parse_args()

    # If config file specified, reload configuration
    if args.config != 'config.py':
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("config", args.config)
            config_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config_module)
            CONFIG = config_module.get_config()
            print(f"✅ Using configuration file: {args.config}")
        except Exception as e:
            print(f"⚠️ Failed to load configuration file: {e}, using default configuration")

    # Create Flask app
    app = create_app(CONFIG)

    # SSL configuration
    ssl_config = CONFIG.get('ssl', {})
    ssl_cert = ssl_config.get('cert_path', '')
    ssl_key = ssl_config.get('key_path', '')
    context = None

    if args.ssl or ssl_config.get('enabled', False):
        if os.path.exists(ssl_cert) and os.path.exists(ssl_key):
            try:
                context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                context.load_cert_chain(ssl_cert, ssl_key)
                # Fix SSL configuration issues
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                # Set more secure SSL options
                context.set_ciphers('ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:!aNULL:!MD5:!DSS')
                context.options |= ssl.OP_NO_SSLv2
                context.options |= ssl.OP_NO_SSLv3
                context.options |= ssl.OP_NO_TLSv1
                context.options |= ssl.OP_NO_TLSv1_1
                print(f"✅ SSL enabled")
            except Exception as e:
                print(f"⚠️ SSL configuration failed: {e}, using HTTP")
                context = None
        else:
            print(f"⚠️ SSL certificates not found, using HTTP")

    # Get base_path for display
    base_path = CONFIG['server'].get('base_path', '')

    # Normalize for display
    if base_path:
        if not base_path.startswith('/'):
            base_path = '/' + base_path
        if not base_path.endswith('/'):
            base_path = base_path + '/'
        access_path = base_path.rstrip('/')
    else:
        access_path = ''

    print(f"🚀 VPN Subscription Converter Service Starting")
    print(f"📍 Access URL: {'https' if context else 'http'}://{args.host}:{args.port}{access_path}")
    print(f"📝 Default Username: {CONFIG['default_user']['username']}")
    print(f"🔑 Default Password: {CONFIG['default_user']['password']}")
    if CONFIG['default_user']['password'] == 'admin':
        print(f"⚠️ Warning: Please change the default password after first login!")

    # Start service
    app.run(
        host=args.host,
        port=args.port,
        ssl_context=context,
        debug=CONFIG['server']['debug']
    )


if __name__ == '__main__':
    main()
