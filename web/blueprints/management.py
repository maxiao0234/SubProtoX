#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Management Blueprint
Handles management interface, rules, settings, and system operations
"""

from flask import Blueprint, request, jsonify, render_template_string, session, current_app, send_from_directory, redirect
import sqlite3
import os
import shutil
import subprocess
import threading
import time
from web.blueprints.auth import login_required
from web.templates.management import MANAGEMENT_HTML
from web.i18n.languages import get_text

management_bp = Blueprint('management', __name__)


@management_bp.route('/')
@login_required
def index():
    """Management interface"""
    converter = current_app.config['CONVERTER']
    config = current_app.config['APP_CONFIG']

    # Get language from query parameter or session
    lang = request.args.get('lang')
    if lang and lang in ['en', 'zh']:
        session['language'] = lang
    elif 'language' not in session:
        session['language'] = 'en'

    current_lang = session['language']

    # Get the tab parameter to restore active tab after language switch
    active_tab = request.args.get('tab', 'converter')

    # Get current username from session
    current_username = session.get('username', config['default_user']['username'])

    # Get current configuration values
    server_port = config['server']['port']
    server_host = config['server']['host']

    # Get SSL configuration status with safe defaults
    ssl_config = config.get('ssl', {})
    ssl_enabled = ssl_config.get('enabled', False)
    ssl_cert_path = ssl_config.get('cert_path', '')
    ssl_key_path = ssl_config.get('key_path', '')

    # Check SSL status and extract domain from certificate path
    ssl_status_text = 'Enabled' if ssl_enabled else 'Disabled'
    ssl_status_class = 'bg-success' if ssl_enabled else 'bg-secondary'
    ssl_status_bg = 'text-bg-success' if ssl_enabled else 'text-bg-secondary'
    ssl_icon = '<span class="material-symbols-outlined" style="font-size: 16px;">lock</span>' if ssl_enabled else '<span class="material-symbols-outlined" style="font-size: 16px;">lock_open</span>'

    # Extract domain from certificate path
    ssl_domain = ''
    if ssl_enabled and ssl_cert_path:
        import re
        # Try to extract domain from certificate path
        match = re.search(r'/([^/]+)\.(pem|crt|cert|bundle\.pem|key)', ssl_cert_path)
        if match:
            domain_part = match.group(1)
            # Remove common suffixes
            domain_part = domain_part.replace('_bundle', '').replace('_cert', '').replace('_key', '')
            ssl_domain = domain_part

    if not ssl_domain:
        ssl_domain = 'Not configured' if current_lang == 'en' else '未配置'

    # SSL options for select
    ssl_enabled_selected = 'selected' if ssl_enabled else ''
    ssl_disabled_selected = '' if ssl_enabled else 'selected'
    ssl_option_enabled = 'HTTPS Enabled' if current_lang == 'en' else 'HTTPS已启用'
    ssl_option_disabled = 'HTTP Only' if current_lang == 'en' else '仅HTTP'

    if current_lang == 'zh':
        ssl_status_text = '已启用' if ssl_enabled else '已禁用'
        ssl_display_status = 'HTTPS已启用' if ssl_enabled else 'HTTP模式'
        ssl_enabled_text = '已启用SSL/TLS加密' if ssl_enabled else '未启用SSL'
    else:
        ssl_display_status = 'HTTPS Enabled' if ssl_enabled else 'HTTP Mode'
        ssl_enabled_text = 'SSL/TLS Encryption Enabled' if ssl_enabled else 'SSL Not Enabled'

    # SSL configuration notes
    ssl_domain_note = ('SSL certificate must match your domain name'
                      if current_lang == 'en' else
                      'SSL证书必须与您的域名匹配')
    ssl_config_note = ('Changes will take effect after restart'
                      if current_lang == 'en' else
                      '更改将在重启后生效')
    ssl_info_title = 'SSL Configuration Info' if current_lang == 'en' else 'SSL配置信息'
    ssl_status_label = 'SSL/HTTPS Status' if current_lang == 'en' else 'SSL/HTTPS状态'
    ssl_domain_label = 'Custom Domain' if current_lang == 'en' else '自定义域名'
    ssl_domain_hint = 'Enter your domain name (e.g., example.com)' if current_lang == 'en' else '输入您的域名（例如：example.com）'
    ssl_current_label = 'Current' if current_lang == 'en' else '当前'
    ssl_cert_hint = 'Full path to SSL certificate file' if current_lang == 'en' else 'SSL证书文件的完整路径'
    ssl_key_hint = 'Full path to SSL private key file' if current_lang == 'en' else 'SSL私钥文件的完整路径'

    # Panel base path labels
    panel_base_path_label = 'Panel URL Base Path' if current_lang == 'en' else '面板URL根路径'
    panel_base_path_hint = 'Enter path segment only (e.g., "subprotox" becomes /subprotox/)' if current_lang == 'en' else '只输入路径段（例如："subprotox" 变成 /subprotox/）'

    # Get and normalize current base_path for display
    current_base_path = config['server'].get('base_path', '')
    if current_base_path:
        # Remove leading and trailing slashes for display
        display_path = current_base_path.strip('/')
        formatted_path = f"/{current_base_path.strip('/')}/" if current_base_path.strip('/') else "/"
    else:
        display_path = ''
        formatted_path = '/'

    panel_base_path_current = f"Current: {formatted_path}" if current_lang == 'en' else f"当前：{formatted_path}"

    # Log configuration values
    log_level = config.get('log', {}).get('level', 'INFO')
    log_file_value = config.get('log', {}).get('file', '')
    access_log_enabled = config.get('log', {}).get('access_log', False)
    debug_mode_enabled = config['server']['debug']

    # Log level selections
    log_level_debug_selected = 'selected' if log_level == 'DEBUG' else ''
    log_level_info_selected = 'selected' if log_level == 'INFO' else ''
    log_level_warning_selected = 'selected' if log_level == 'WARNING' else ''
    log_level_error_selected = 'selected' if log_level == 'ERROR' else ''

    # Checkbox states
    access_log_checked = 'checked' if access_log_enabled else ''
    debug_mode_checked = 'checked' if debug_mode_enabled else ''

    return render_template_string(
        MANAGEMENT_HTML,
        lang=current_lang,
        title=get_text('title', current_lang),
        logout_btn=get_text('logout_btn', current_lang),
        main_title=get_text('main_title', current_lang),
        main_subtitle=get_text('main_subtitle', current_lang),
        features_ssl=get_text('features.ssl', current_lang),
        features_realtime=get_text('features.realtime', current_lang),
        features_rules=get_text('features.rules', current_lang),
        features_routing=get_text('features.routing', current_lang),
        tabs_converter=get_text('tabs.converter', current_lang),
        tabs_history=get_text('tabs.history', current_lang),
        tabs_rules=get_text('tabs.rules', current_lang),
        tabs_settings=get_text('tabs.settings', current_lang),
        tabs_api=get_text('tabs.api', current_lang),
        converter_page_title=get_text('converter.page_title', current_lang),
        converter_page_subtitle=get_text('converter.page_subtitle', current_lang),
        converter_select_conversion_mode=get_text('converter.select_conversion_mode', current_lang),
        converter_proxy_links=get_text('converter.proxy_links', current_lang),
        converter_proxy_links_desc=get_text('converter.proxy_links_desc', current_lang),
        converter_support_node_editing=get_text('converter.support_node_editing', current_lang),
        converter_subscription_url=get_text('converter.subscription_url', current_lang),
        converter_subscription_url_desc=get_text('converter.subscription_url_desc', current_lang),
        converter_one_step_conversion=get_text('converter.one_step_conversion', current_lang),
        converter_paste_proxy_links=get_text('converter.paste_proxy_links', current_lang),
        converter_paste_subscription_url=get_text('converter.paste_subscription_url', current_lang),
        converter_basic_configuration=get_text('converter.basic_configuration', current_lang),
        converter_subscription_settings=get_text('converter.subscription_settings', current_lang),
        converter_custom_name_hint=get_text('converter.custom_name_hint', current_lang),
        converter_rule_types=get_text('converter.rule_types', current_lang),
        converter_built_in=get_text('converter.built_in', current_lang),
        converter_custom=get_text('converter.custom', current_lang),
        converter_link_title=get_text('converter.link_title', current_lang),
        converter_link_input_label=get_text('converter.link_input_label', current_lang),
        converter_config_name=get_text('converter.config_name', current_lang),
        converter_config_placeholder=get_text('converter.config_placeholder', current_lang),
        converter_config_default=get_text('converter.config_default', current_lang),
        converter_rule_template=get_text('converter.rule_template', current_lang),
        converter_convert_btn=get_text('converter.convert_btn', current_lang),
        converter_node_preview=get_text('converter.node_preview', current_lang),
        converter_node_type=get_text('converter.node_type', current_lang),
        converter_node_server=get_text('converter.node_server', current_lang),
        converter_node_name=get_text('converter.node_name', current_lang),
        converter_generate_btn=get_text('converter.generate_btn', current_lang),
        converter_sub_title=get_text('converter.sub_title', current_lang),
        converter_sub_input_label=get_text('converter.sub_input_label', current_lang),
        converter_sub_config_name=get_text('converter.sub_config_name', current_lang),
        converter_sub_placeholder=get_text('converter.sub_placeholder', current_lang),
        converter_sub_default=get_text('converter.sub_default', current_lang),
        converter_sub_convert_btn=get_text('converter.sub_convert_btn', current_lang),
        converter_result_title=get_text('converter.result_title', current_lang),
        converter_copy_btn=get_text('converter.copy_btn', current_lang),
        converter_download_btn=get_text('converter.download_btn', current_lang),
        converter_auto_update=get_text('converter.auto_update', current_lang),
        converter_update_interval=get_text('converter.update_interval', current_lang),
        converter_traffic_limit=get_text('converter.traffic_limit', current_lang),
        converter_enable_periodic_refresh=get_text('converter.enable_periodic_refresh', current_lang),
        converter_zero_unlimited=get_text('converter.zero_unlimited', current_lang),
        converter_subscription_link=get_text('converter.subscription_link', current_lang),
        converter_one_link_per_line=get_text('converter.one_link_per_line', current_lang),
        converter_interval_minutes=get_text('converter.interval_minutes', current_lang),
        converter_interval_hours=get_text('converter.interval_hours', current_lang),
        converter_interval_days=get_text('converter.interval_days', current_lang),
        converter_interval_zero_no_update=get_text('converter.interval_zero_no_update', current_lang),
        rules_rule_name=get_text('rules.rule_name', current_lang),
        rules_rule_desc=get_text('rules.rule_desc', current_lang),
        rules_rule_content=get_text('rules.rule_content', current_lang),
        rules_save=get_text('rules.save', current_lang),
        rules_cancel=get_text('rules.cancel', current_lang),
        rules_failed_to_get='Failed to get rule: ' if current_lang == 'en' else '获取规则失败: ',
        alerts_unknown_error=get_text('alerts.unknown_error', current_lang),
        alerts_link_copied=get_text('alerts.link_copied', current_lang),
        alerts_enter_links=get_text('alerts.enter_links', current_lang),
        alerts_parse_failed=get_text('alerts.parse_failed', current_lang),
        alerts_no_nodes=get_text('alerts.no_nodes', current_lang),
        alerts_config_failed=get_text('alerts.config_failed', current_lang),
        alerts_enter_sub=get_text('alerts.enter_sub', current_lang),
        alerts_convert_failed=get_text('alerts.convert_failed', current_lang),
        alerts_history_clear_failed=get_text('alerts.history_clear_failed', current_lang),
        alerts_rule_get_failed=get_text('alerts.rule_get_failed', current_lang),
        alerts_rule_create_failed=get_text('alerts.rule_create_failed', current_lang),
        alerts_restart_failed=get_text('alerts.restart_failed', current_lang),
        rules_create_success=get_text('rules.create_success', current_lang),
        rules_name_empty=get_text('rules.name_empty', current_lang),
        rules_content_empty=get_text('rules.content_empty', current_lang),
        history_cleared=get_text('history.history_cleared', current_lang),
        history_page_title=get_text('history.page_title', current_lang),
        history_page_subtitle=get_text('history.page_subtitle', current_lang),
        history_records=get_text('history.history_records', current_lang),
        history_token=get_text('history.token', current_lang),
        history_subscription_link=get_text('history.subscription_link', current_lang),
        history_created=get_text('history.created', current_lang),
        history_nodes=get_text('history.nodes', current_lang),
        history_view=get_text('history.view', current_lang),
        history_copy=get_text('history.copy', current_lang),
        history_download=get_text('history.download', current_lang),
        history_delete=get_text('history.delete', current_lang),
        history_clear_all=get_text('history.clear_all', current_lang),
        alerts_modal_restart_title=get_text('alerts.modal_restart_title', current_lang),
        alerts_modal_restart_message=get_text('alerts.modal_restart_message', current_lang),
        alerts_modal_restart_confirm=get_text('alerts.modal_restart_confirm', current_lang),
        alerts_modal_clear_title=get_text('alerts.modal_clear_title', current_lang),
        alerts_modal_clear_message=get_text('alerts.modal_clear_message', current_lang),
        alerts_modal_clear_confirm=get_text('alerts.modal_clear_confirm', current_lang),
        alerts_modal_delete_history_title=get_text('alerts.modal_delete_history_title', current_lang),
        alerts_modal_delete_history_message=get_text('alerts.modal_delete_history_message', current_lang),
        alerts_modal_delete_confirm=get_text('alerts.modal_delete_confirm', current_lang),
        alerts_modal_restore_title=get_text('alerts.modal_restore_title', current_lang),
        alerts_modal_restore_message=get_text('alerts.modal_restore_message', current_lang),
        alerts_modal_restore_confirm=get_text('alerts.modal_restore_confirm', current_lang),
        alerts_modal_save_title=get_text('alerts.modal_save_title', current_lang),
        alerts_modal_save_message=get_text('alerts.modal_save_message', current_lang),
        alerts_modal_save_confirm=get_text('alerts.modal_save_confirm', current_lang),
        alerts_modal_template_imported=get_text('alerts.modal_template_imported', current_lang),
        alerts_modal_template_imported_message=get_text('alerts.modal_template_imported_message', current_lang),
        alerts_modal_ok=get_text('alerts.modal_ok', current_lang),
        alerts_modal_cancel=get_text('alerts.modal_cancel', current_lang),
        alerts_modal_save_settings_title=get_text('alerts.modal_save_settings_title', current_lang),
        alerts_modal_save_settings_message=get_text('alerts.modal_save_settings_message', current_lang),
        alerts_modal_settings_saved_title=get_text('alerts.modal_settings_saved_title', current_lang),
        alerts_modal_settings_saved_message=get_text('alerts.modal_settings_saved_message', current_lang),
        alerts_modal_restart_now_title=get_text('alerts.modal_restart_now_title', current_lang),
        alerts_modal_restart_now_message=get_text('alerts.modal_restart_now_message', current_lang),
        alerts_modal_update_account_title=get_text('alerts.modal_update_account_title', current_lang),
        alerts_modal_update_account_message=get_text('alerts.modal_update_account_message', current_lang),
        alerts_modal_account_updated_title=get_text('alerts.modal_account_updated_title', current_lang),
        alerts_modal_account_updated_message=get_text('alerts.modal_account_updated_message', current_lang),
        alerts_modal_save_conversion_title=get_text('alerts.modal_save_conversion_title', current_lang),
        alerts_modal_save_conversion_message=get_text('alerts.modal_save_conversion_message', current_lang),
        alerts_modal_conversion_saved_title=get_text('alerts.modal_conversion_saved_title', current_lang),
        alerts_modal_conversion_saved_message=get_text('alerts.modal_conversion_saved_message', current_lang),
        alerts_modal_clean_records_title=get_text('alerts.modal_clean_records_title', current_lang),
        alerts_modal_clean_records_message=get_text('alerts.modal_clean_records_message', current_lang),
        alerts_modal_records_cleaned_title=get_text('alerts.modal_records_cleaned_title', current_lang),
        alerts_modal_records_cleaned_message=get_text('alerts.modal_records_cleaned_message', current_lang),
        alerts_modal_optimize_db_title=get_text('alerts.modal_optimize_db_title', current_lang),
        alerts_modal_optimize_db_message=get_text('alerts.modal_optimize_db_message', current_lang),
        alerts_modal_db_optimized_title=get_text('alerts.modal_db_optimized_title', current_lang),
        alerts_modal_db_optimized_message=get_text('alerts.modal_db_optimized_message', current_lang),
        alerts_modal_export_backup_title=get_text('alerts.modal_export_backup_title', current_lang),
        alerts_modal_export_backup_message=get_text('alerts.modal_export_backup_message', current_lang),
        alerts_modal_backup_exported_title=get_text('alerts.modal_backup_exported_title', current_lang),
        alerts_modal_backup_exported_message=get_text('alerts.modal_backup_exported_message', current_lang),
        rules_create_new=get_text('rules.create_new', current_lang),
        rules_delete=get_text('rules.delete', current_lang),
        rules_page_title=get_text('rules_page.page_title', current_lang),
        rules_page_subtitle=get_text('rules_page.page_subtitle', current_lang),
        rules_built_in_templates=get_text('rules_page.built_in_templates', current_lang),
        rules_custom_rules=get_text('rules_page.custom_rules', current_lang),
        rules_editing_guide=get_text('rules_page.rule_editing_guide', current_lang),
        rules_built_in_desc=get_text('rules_page.built_in_desc', current_lang),
        rules_custom_desc=get_text('rules_page.custom_desc', current_lang),
        rules_quick_tips=get_text('rules_page.quick_tips', current_lang),
        rules_quick_tip_1=get_text('rules_page.quick_tip_1', current_lang),
        rules_quick_tip_2=get_text('rules_page.quick_tip_2', current_lang),
        rules_quick_tip_3=get_text('rules_page.quick_tip_3', current_lang),
        rules_syntax_reference=get_text('rules_page.rule_syntax_reference', current_lang),
        rules_syntax_domain=get_text('rules_page.syntax_domain', current_lang),
        rules_syntax_domain_desc=get_text('rules_page.syntax_domain_desc', current_lang),
        rules_syntax_domain_suffix=get_text('rules_page.syntax_domain_suffix', current_lang),
        rules_syntax_domain_suffix_desc=get_text('rules_page.syntax_domain_suffix_desc', current_lang),
        rules_syntax_ip_cidr=get_text('rules_page.syntax_ip_cidr', current_lang),
        rules_syntax_ip_cidr_desc=get_text('rules_page.syntax_ip_cidr_desc', current_lang),
        rules_syntax_domain_matching=get_text('rules_page.syntax_domain_matching', current_lang),
        rules_syntax_ip_geo_matching=get_text('rules_page.syntax_ip_geo_matching', current_lang),
        rules_syntax_advanced_rules=get_text('rules_page.syntax_advanced_rules', current_lang),
        rules_syntax_match_wildcard=get_text('rules_page.syntax_match_wildcard', current_lang),
        rules_syntax_exact_match=get_text('rules_page.syntax_exact_match', current_lang),
        rules_syntax_private_ip=get_text('rules_page.syntax_private_ip', current_lang),
        rules_syntax_china_ips=get_text('rules_page.syntax_china_ips', current_lang),
        rules_quick_tip_one_rule=get_text('rules_page.quick_tip_one_rule', current_lang),
        rules_quick_tip_for_comments=get_text('rules_page.quick_tip_for_comments', current_lang),
        rules_quick_tip_top_to_bottom=get_text('rules_page.quick_tip_top_to_bottom', current_lang),
        rules_quick_tip_end_with_match=get_text('rules_page.quick_tip_end_with_match', current_lang),
        rules_quick_tip_as_fallback=get_text('rules_page.quick_tip_as_fallback', current_lang),
        rules_syntax_by_process=get_text('rules_page.syntax_by_process', current_lang),
        rules_syntax_catch_all=get_text('rules_page.syntax_catch_all', current_lang),
        rules_rule_name_col=get_text('rules_page.rule_name', current_lang),
        rules_rule_description_col=get_text('rules_page.rule_description', current_lang),
        rules_rule_content_col=get_text('rules_page.rule_content', current_lang),
        rules_restore=get_text('rules_page.restore', current_lang),
        rules_no_custom_rules=get_text('rules_page.no_custom_rules', current_lang),
        api_page_title=get_text('api.page_title', current_lang),
        api_page_subtitle=get_text('api.page_subtitle', current_lang),
        api_auth_required=get_text('api.auth_required', current_lang),
        api_auth_guide=get_text('api.auth_guide', current_lang),
        api_auth_protected=get_text('api.auth_protected', current_lang),
        api_auth_public=get_text('api.auth_public', current_lang),
        api_authenticated_endpoints=get_text('api.authenticated_endpoints', current_lang),
        api_authenticated_endpoints_desc=get_text('api.authenticated_endpoints_desc', current_lang),
        api_public_access=get_text('api.public_access', current_lang),
        api_public_access_desc=get_text('api.public_access_desc', current_lang),
        api_built_in_templates=get_text('api.built_in_templates', current_lang),
        api_quick_tips=get_text('api.quick_tips', current_lang),
        api_quick_tips_session=get_text('api.quick_tips_session', current_lang),
        api_quick_tips_cookie=get_text('api.quick_tips_cookie', current_lang),
        api_quick_tips_default=get_text('api.quick_tips_default', current_lang),
        api_endpoint_1_title=get_text('api.endpoint_1_title', current_lang),
        api_endpoint_1_desc=get_text('api.endpoint_1_desc', current_lang),
        api_endpoint_2_title=get_text('api.endpoint_2_title', current_lang),
        api_endpoint_2_desc=get_text('api.endpoint_2_desc', current_lang),
        api_endpoint_3_title=get_text('api.endpoint_3_title', current_lang),
        api_endpoint_3_desc=get_text('api.endpoint_3_desc', current_lang),
        api_endpoint_4_title=get_text('api.endpoint_4_title', current_lang),
        api_endpoint_4_desc=get_text('api.endpoint_4_desc', current_lang),
        api_description=get_text('api.description', current_lang),
        api_request_body=get_text('api.request_body', current_lang),
        api_query_parameters=get_text('api.query_parameters', current_lang),
        api_path_parameters=get_text('api.path_parameters', current_lang),
        api_response=get_text('api.response', current_lang),
        api_example=get_text('api.example', current_lang),
        api_response_yaml_headers=get_text('api.response_yaml_headers', current_lang),
        api_history_management=get_text('api.history_management', current_lang),
        api_history_get_all=get_text('api.history_get_all', current_lang),
        api_history_delete_one=get_text('api.history_delete_one', current_lang),
        api_history_clear_all=get_text('api.history_clear_all', current_lang),
        api_rules_management=get_text('api.rules_management', current_lang),
        api_rules_list_all=get_text('api.rules_list_all', current_lang),
        api_rules_create=get_text('api.rules_create', current_lang),
        api_rules_get_one=get_text('api.rules_get_one', current_lang),
        api_rules_update=get_text('api.rules_update', current_lang),
        api_rules_delete=get_text('api.rules_delete', current_lang),
        api_template_default_zh=get_text('api.template_default_zh', current_lang),
        api_template_default=get_text('api.template_default', current_lang),
        api_template_research=get_text('api.template_research', current_lang),
        api_template_minimal=get_text('api.template_minimal', current_lang),
        api_copy=get_text('api.copy', current_lang),
        api_copied=get_text('api.copied', current_lang),
        settings_system_config=get_text('settings.system_config', current_lang),
        settings_server_port=get_text('settings.server_port', current_lang),
        settings_listen_address=get_text('settings.listen_address', current_lang),
        settings_ssl_cert_path=get_text('settings.ssl_cert_path', current_lang),
        settings_ssl_key_path=get_text('settings.ssl_key_path', current_lang),
        settings_ssl_cert_hint=ssl_cert_hint,
        settings_ssl_key_hint=ssl_key_hint,
        ssl_cert_value=ssl_cert_path if ssl_enabled else '',
        ssl_key_value=ssl_key_path if ssl_enabled else '',
        ssl_status_text=ssl_status_text,
        ssl_status_class=ssl_status_class,
        ssl_status_bg=ssl_status_bg,
        ssl_icon=ssl_icon,
        ssl_display_status=ssl_display_status,
        ssl_enabled_text=ssl_enabled_text,
        ssl_enabled_selected=ssl_enabled_selected,
        ssl_disabled_selected=ssl_disabled_selected,
        ssl_option_enabled=ssl_option_enabled,
        ssl_option_disabled=ssl_option_disabled,
        ssl_domain=ssl_domain if ssl_domain != 'Not configured' and ssl_domain != '未配置' else '',
        settings_ssl_info_title=ssl_info_title,
        settings_ssl_status=ssl_status_label,
        settings_ssl_status_label=ssl_status_label,
        settings_ssl_domain_label=ssl_domain_label,
        settings_ssl_domain_hint=ssl_domain_hint,
        settings_ssl_current=ssl_current_label,
        settings_ssl_domain_note=ssl_domain_note,
        settings_ssl_config_note=ssl_config_note,
        settings_enable_debug=get_text('settings.enable_debug', current_lang),
        settings_save_system=get_text('settings.save_system', current_lang),
        settings_account_settings=get_text('settings.account_settings', current_lang),
        settings_current_password=get_text('settings.current_password', current_lang),
        settings_enter_current_password='Enter current password' if current_lang == 'en' else '输入当前密码',
        settings_new_username=get_text('settings.new_username', current_lang),
        settings_new_password=get_text('settings.new_password', current_lang),
        settings_keep_current='Leave blank to keep current' if current_lang == 'en' else '留空保持当前',
        settings_confirm_password=get_text('settings.confirm_password', current_lang),
        settings_reenter_password='Re-enter new password' if current_lang == 'en' else '重新输入新密码',
        settings_update_account=get_text('settings.update_account', current_lang),
        settings_current_info=get_text('settings.current_info', current_lang),
        settings_session_timeout='Session timeout: 24 hours' if current_lang == 'en' else '会话超时: 24小时',
        settings_last_login='Last login: Today' if current_lang == 'en' else '最后登录: 今天',
        settings_security_tips=get_text('settings.security_tips', current_lang),
        settings_tip1='Use strong passwords' if current_lang == 'en' else '使用强密码',
        settings_tip2='Change password regularly' if current_lang == 'en' else '定期更换密码',
        settings_tip3='Re-login required after changes' if current_lang == 'en' else '更改后需要重新登录',
        settings_conversion_settings=get_text('settings.conversion_settings', current_lang),
        settings_max_proxies=get_text('settings.max_proxies', current_lang),
        settings_max_proxies_hint='Maximum number of proxies in one config' if current_lang == 'en' else '单个配置最大代理数',
        settings_conv_timeout=get_text('settings.conv_timeout', current_lang),
        settings_timeout_hint='Timeout for subscription fetching' if current_lang == 'en' else '订阅获取超时',
        settings_user_agent=get_text('settings.user_agent', current_lang),
        settings_user_agent_hint='User agent for HTTP requests' if current_lang == 'en' else 'HTTP请求的用户代理',
        settings_save_conversion=get_text('settings.save_conversion', current_lang),
        settings_db_maintenance=get_text('settings.db_maintenance', current_lang),
        settings_history_records=get_text('settings.history_records', current_lang),
        settings_clean_old_desc=get_text('settings.clean_old_desc', current_lang),
        settings_clean_old=get_text('settings.clean_old', current_lang),
        settings_db_optimize=get_text('settings.db_optimize', current_lang),
        settings_optimize_desc=get_text('settings.optimize_desc', current_lang),
        settings_optimize_db=get_text('settings.optimize_db', current_lang),
        settings_export_backup=get_text('settings.export_backup', current_lang),
        settings_backup_desc=get_text('settings.backup_desc', current_lang),
        settings_export=get_text('settings.export', current_lang),
        settings_current_port='Current port' if current_lang == 'en' else '当前端口',
        settings_current_host='Current' if current_lang == 'en' else '当前',
        server_port=server_port,
        server_host=server_host,
        current_username=current_username,
        panel_base_path_label=panel_base_path_label,
        panel_base_path_hint=panel_base_path_hint,
        panel_base_path_current=panel_base_path_current,
        panel_base_path=display_path,  # Display without slashes
        settings_page_title=get_text('settings.page_title', current_lang),
        settings_page_subtitle=get_text('settings.page_subtitle', current_lang),
        settings_basic_service=get_text('settings.basic_service', current_lang),
        settings_ssl_https_config=get_text('settings.ssl_https_config', current_lang),
        settings_logging_monitoring=get_text('settings.logging_monitoring', current_lang),
        settings_debug_mode=get_text('settings.debug_mode', current_lang),
        settings_log_level=get_text('settings.log_level', current_lang),
        settings_log_level_hint=get_text('settings.log_level_hint', current_lang),
        settings_log_file=get_text('settings.log_file', current_lang),
        settings_log_file_hint=get_text('settings.log_file_hint', current_lang),
        settings_enable_access_log=get_text('settings.enable_access_log', current_lang),
        settings_access_log_hint=get_text('settings.access_log_hint', current_lang),
        settings_debug_warning_title=get_text('settings.debug_warning_title', current_lang),
        settings_debug_warning_1=get_text('settings.debug_warning_1', current_lang),
        settings_debug_warning_2=get_text('settings.debug_warning_2', current_lang),
        settings_debug_warning_3=get_text('settings.debug_warning_3', current_lang),
        log_file_value=log_file_value,
        log_level_debug_selected=log_level_debug_selected,
        log_level_info_selected=log_level_info_selected,
        log_level_warning_selected=log_level_warning_selected,
        log_level_error_selected=log_level_error_selected,
        access_log_checked=access_log_checked,
        debug_mode_checked=debug_mode_checked,
        restart_btn=get_text('restart_btn', current_lang),
        # JavaScript alert texts for settings
        ssl_validation_empty='SSL certificate and key paths are required when SSL is enabled' if current_lang == 'en' else 'SSL启用时证书和密钥路径必填',
        ssl_validation_domain='Domain name is required when SSL is enabled' if current_lang == 'en' else 'SSL启用时域名必填',
        base_path_validation='Base path must start and end with / (e.g., /subprotox/)' if current_lang == 'en' else '根路径必须以 / 开头和结尾（例如：/subprotox/）',
        settings_saved_success='Settings saved successfully' if current_lang == 'en' else '设置保存成功',
        settings_restart_required='Restart required for changes to take effect' if current_lang == 'en' else '需要重启以使更改生效',
        settings_restart_now='Restart service now?' if current_lang == 'en' else '立即重启服务？',
        settings_save_failed='Failed to save settings' if current_lang == 'en' else '保存设置失败',
        settings_new_url_label='New URL: ' if current_lang == 'en' else '新URL: ',
        settings_manual_restart='Please manually restart the service (Ctrl+C and run again) to apply the change.' if current_lang == 'en' else '请手动重启服务（Ctrl+C 并重新运行）以应用更改。',
        settings_failed_prefix='Failed to save settings: ' if current_lang == 'en' else '保存设置失败: ',
        rule_restored_success='has been successfully restored to default state' if current_lang == 'en' else '已成功恢复到默认状态',
        rule_name_empty='Rule name cannot be empty' if current_lang == 'en' else '规则名称不能为空',
        rule_content_empty='Rule content cannot be empty' if current_lang == 'en' else '规则内容不能为空',
        rule_updated_success='Rule updated successfully' if current_lang == 'en' else '规则更新成功',
        rule_delete_confirm='Are you sure to delete this rule?' if current_lang == 'en' else '确定要删除这条规则吗？',
        delete_success='Delete successful' if current_lang == 'en' else '删除成功',
        account_password_required='Please enter current password for verification' if current_lang == 'en' else '请输入当前密码进行验证',
        account_password_mismatch='New passwords do not match' if current_lang == 'en' else '新密码不匹配',
        account_change_required='Please enter new username or new password, at least one modification required' if current_lang == 'en' else '请输入新用户名或新密码，至少需要一项修改',
        account_update_failed_prefix='Update failed: ' if current_lang == 'en' else '更新失败: ',
        unknown_error='Unknown error' if current_lang == 'en' else '未知错误',
        en_selected='selected' if current_lang == 'en' else '',
        zh_selected='selected' if current_lang == 'zh' else '',
        current_lang_display='EN' if current_lang == 'en' else '中文',
        active_tab=active_tab
    )


@management_bp.route('/api/rules', methods=['GET', 'POST'])
@login_required
def handle_rules():
    """Rule management"""
    converter = current_app.config['CONVERTER']
    db_path = converter.db_path

    if request.method == 'GET':
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Define built-in template rule names
        builtin_names = ['Default Routing', 'Default Routing (Chinese Interface)', 'Academic & Research Routing', 'Minimal Rules']

        # Get built-in templates in specific order
        builtin_rules = []
        for name in builtin_names:
            c.execute('SELECT id, name, description FROM rules WHERE name = ?', (name,))
            row = c.fetchone()
            if row:
                builtin_rules.append({
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'is_builtin': True
                })

        # Get custom rules (excluding built-in ones)
        placeholders = ','.join(['?' for _ in builtin_names])
        c.execute(f'SELECT id, name, description FROM rules WHERE name NOT IN ({placeholders}) ORDER BY name', builtin_names)
        custom_rules = []
        for row in c.fetchall():
            custom_rules.append({
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'is_builtin': False
            })
        conn.close()

        return jsonify({
            'builtin': builtin_rules,
            'custom': custom_rules
        })

    else:  # POST
        data = request.json
        name = data.get('name')
        description = data.get('description', '')
        content = data.get('content', '')

        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        try:
            c.execute(
                'INSERT INTO rules (name, description, content) VALUES (?, ?, ?)',
                (name, description, content)
            )
            conn.commit()
            conn.close()
            return jsonify({'success': True})
        except:
            conn.close()
            return jsonify({'error': 'Rule name already exists'}), 400


@management_bp.route('/api/rules/<int:rule_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def handle_rule(rule_id):
    """Handle individual rule operations"""
    converter = current_app.config['CONVERTER']
    db_path = converter.db_path
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    if request.method == 'GET':
        # Get rule details
        c.execute('SELECT id, name, description, content FROM rules WHERE id = ?', (rule_id,))
        row = c.fetchone()
        conn.close()

        if not row:
            return jsonify({'error': 'Rule not found'}), 404

        return jsonify({
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'content': row[3]
        })

    elif request.method == 'PUT':
        # Update rule
        data = request.json
        name = data.get('name')
        description = data.get('description', '')
        content = data.get('content', '')

        try:
            c.execute(
                'UPDATE rules SET name = ?, description = ?, content = ? WHERE id = ?',
                (name, description, content, rule_id)
            )
            conn.commit()
            conn.close()
            return jsonify({'success': True})
        except Exception as e:
            conn.close()
            return jsonify({'error': 'Update failed, rule name may already exist'}), 400

    elif request.method == 'DELETE':
        # Delete rule
        c.execute('DELETE FROM rules WHERE id = ?', (rule_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})


@management_bp.route('/api/rules/by-name/<rule_name>', methods=['GET'])
@login_required
def get_rule_by_name(rule_name):
    """Get a rule by its name (used for importing templates)"""
    converter = current_app.config['CONVERTER']
    db_path = converter.db_path

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT id, name, description, content FROM rules WHERE name = ?', (rule_name,))
    row = c.fetchone()
    conn.close()

    if not row:
        return jsonify({'error': 'Rule not found'}), 404

    return jsonify({
        'id': row[0],
        'name': row[1],
        'description': row[2],
        'content': row[3]
    })


@management_bp.route('/api/rules/<int:rule_id>/restore', methods=['POST'])
@login_required
def restore_rule(rule_id):
    """Restore a built-in rule to its default state"""
    converter = current_app.config['CONVERTER']
    rule_manager = converter.rule_manager
    db_path = converter.db_path

    if not rule_manager:
        return jsonify({'error': 'Rule manager not available'}), 500

    # Get rule name from database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT name FROM rules WHERE id = ?', (rule_id,))
    result = c.fetchone()

    if not result:
        conn.close()
        return jsonify({'error': 'Rule not found'}), 404

    rule_name = result[0]

    # Check if it's a built-in rule
    builtin_names = ['Default Routing', 'Default Routing (Chinese Interface)', 'Academic & Research Routing', 'Minimal Rules']
    if rule_name not in builtin_names:
        conn.close()
        return jsonify({'error': 'Only built-in rules can be restored'}), 400

    # Get default content from rule manager
    try:
        default_rules = rule_manager.get_rules_by_name(rule_name)
        default_content = '\n'.join(default_rules)

        # Get default description
        rule_info = rule_manager.get_rule_info(rule_name)
        default_description = rule_info.get('description', '') if rule_info else ''

        # Update database with default content
        c.execute(
            'UPDATE rules SET content = ?, description = ? WHERE id = ?',
            (default_content, default_description, rule_id)
        )
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Rule restored successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'error': f'Failed to restore rule: {str(e)}'}), 500


@management_bp.route('/api/change-account', methods=['POST'])
@login_required
def change_account():
    """Change account information"""
    converter = current_app.config['CONVERTER']
    data = request.json
    current_password = data.get('current_password')
    new_username = data.get('new_username')
    new_password = data.get('new_password')

    username = session.get('username', current_app.config['APP_CONFIG']['default_user']['username'])

    # Verify current password
    if not converter.verify_user(username, current_password):
        return jsonify({'error': 'Current password incorrect'}), 400

    # Update account information
    success = converter.change_account(username, new_username, new_password)

    if not success:
        return jsonify({'error': 'Update failed, username may already exist'}), 400

    # Clear session
    session.clear()

    return jsonify({'success': True})


@management_bp.route('/api/settings/system', methods=['POST'])
@login_required
def save_system_settings():
    """Save system settings"""
    data = request.json
    port = data.get('port')
    host = data.get('host')
    base_path_input = (data.get('base_path') or '').strip()  # Handle None and empty string
    ssl_enabled = data.get('ssl_enabled', False)
    ssl_domain = data.get('ssl_domain')
    ssl_cert_path = data.get('ssl_cert_path')
    ssl_key_path = data.get('ssl_key_path')
    log_level = data.get('log_level')
    log_file = data.get('log_file')
    access_log = data.get('access_log', False)
    debug_mode = data.get('debug_mode', False)

    # Normalize base_path: user inputs "subprotox", we store as empty string (no prefix)
    # If user wants prefix, they input the segment only
    if base_path_input:
        # Remove any slashes user might have added
        base_path = base_path_input.strip('/')
    else:
        # Empty input means root path (no base_path in config)
        base_path = ''

    # Validate SSL settings if enabled
    if ssl_enabled:
        if not ssl_cert_path or not ssl_key_path:
            return jsonify({'error': 'SSL certificate and key paths are required when SSL is enabled'}), 400

        # Check if certificate files exist
        if not os.path.exists(ssl_cert_path):
            return jsonify({'error': f'SSL certificate file not found: {ssl_cert_path}'}), 400

        if not os.path.exists(ssl_key_path):
            return jsonify({'error': f'SSL key file not found: {ssl_key_path}'}), 400

    # Read current config.py
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'config.py')
    backup_path = config_path + '.backup'

    try:
        # Backup current config
        shutil.copy2(config_path, backup_path)

        # Read config file
        with open(config_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Update configuration values
        new_lines = []
        in_server_config = False
        in_ssl_config = False
        in_log_config = False
        has_base_path = False

        for line in lines:
            # Update server configuration
            if 'SERVER_CONFIG = {' in line:
                in_server_config = True
                new_lines.append(line)
            elif in_server_config and '}' in line:
                # Add base_path before closing brace if it doesn't exist
                if not has_base_path:
                    # Check if last line ends with comma
                    if new_lines and new_lines[-1].strip().endswith(','):
                        new_lines.append(f"    'base_path': '{base_path}'  # Panel URL path segment (e.g., 'subprotox' becomes /subprotox/)\n")
                    else:
                        # Add comma to last line first
                        if new_lines:
                            new_lines[-1] = new_lines[-1].rstrip('\n') + ',\n'
                        new_lines.append(f"    'base_path': '{base_path}'  # Panel URL path segment (e.g., 'subprotox' becomes /subprotox/)\n")
                in_server_config = False
                new_lines.append(line)
            elif in_server_config:
                if "'port':" in line and port:
                    new_lines.append(f"    'port': {port},\n")
                elif "'host':" in line and host:
                    new_lines.append(f"    'host': '{host}',\n")
                elif "'debug':" in line:
                    new_lines.append(f"    'debug': {str(debug_mode)},\n")
                elif "'base_path':" in line:
                    has_base_path = True
                    # Always keep base_path, even if empty
                    new_lines.append(f"    'base_path': '{base_path}'  # Panel URL path segment (e.g., 'subprotox' becomes /subprotox/)\n")
                else:
                    new_lines.append(line)
            # Update SSL configuration
            elif 'SSL_CONFIG = {' in line:
                in_ssl_config = True
                new_lines.append(line)
            elif in_ssl_config and '}' in line:
                in_ssl_config = False
                new_lines.append(line)
            elif in_ssl_config:
                if "'enabled':" in line:
                    new_lines.append(f"    'enabled': {str(ssl_enabled)},  # Enable HTTPS\n")
                elif "'cert_path':" in line:
                    cert_value = ssl_cert_path if ssl_cert_path else ''
                    new_lines.append(f"    'cert_path': '{cert_value}',  # SSL certificate path\n")
                elif "'key_path':" in line:
                    key_value = ssl_key_path if ssl_key_path else ''
                    new_lines.append(f"    'key_path': '{key_value}',   # SSL private key path\n")
                elif "'domain':" in line:
                    domain_value = ssl_domain if ssl_domain else ''
                    new_lines.append(f"    'domain': '{domain_value}'      # Custom domain (optional)\n")
                else:
                    new_lines.append(line)
            # Update LOG configuration
            elif 'LOG_CONFIG = {' in line:
                in_log_config = True
                new_lines.append(line)
            elif in_log_config and '}' in line:
                in_log_config = False
                new_lines.append(line)
            elif in_log_config:
                if "'level':" in line and log_level:
                    new_lines.append(f"    'level': '{log_level}',\n")
                elif "'file':" in line:
                    # Treat empty string and 'None' string as None
                    if log_file and log_file != 'None':
                        new_lines.append(f"    'file': '{log_file}',\n")
                    else:
                        new_lines.append(f"    'file': None  # Log file path, None means output to console\n")
                elif "'access_log':" in line:
                    new_lines.append(f"    'access_log': {str(access_log)}\n")
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)

        # Write updated config
        with open(config_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

        # Check if base_path was changed
        old_base_path = current_app.config['APP_CONFIG']['server'].get('base_path', '')
        base_path_changed = base_path != old_base_path

        if base_path_changed:
            message = 'Settings saved. IMPORTANT: Panel URL Base Path changed. Please manually restart the service and access the new URL.'
        else:
            message = 'Settings saved successfully. Click Restart to apply changes.'

        return jsonify({
            'success': True,
            'message': message,
            'base_path_changed': base_path_changed,
            'new_base_path': f"/{base_path}/" if base_path else "/"
        })

    except Exception as e:
        # Restore backup on error
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, config_path)
        return jsonify({'error': f'Failed to save settings: {str(e)}'}), 500


@management_bp.route('/api/restart', methods=['POST'])
@login_required
def restart_service():
    """Restart service"""
    def restart():
        """Execute restart in background"""
        time.sleep(2)  # Give time for response to be sent

        try:
            # Check if running as systemd service (use full path)
            result = subprocess.run(['/usr/bin/systemctl', 'is-active', 'subprotox'],
                                  capture_output=True, text=True, timeout=2)

            if result.returncode == 0:
                # Running as systemd service, restart directly with sudo
                subprocess.run(['/usr/bin/sudo', '/usr/bin/systemctl', 'restart', 'subprotox'],
                             check=False,
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
                return
        except Exception as e:
            # Log the error but continue to manual restart
            print(f"Failed to restart via systemd: {e}")
            pass

        # Not running as systemd service, restart the python process directly
        import sys
        import signal

        # Get current process PID and command line
        pid = os.getpid()
        python = sys.executable
        args = sys.argv.copy()

        # Create a restart script that will run after this process exits
        restart_script = f'''#!/bin/bash
sleep 2
cd {os.getcwd()}
source venv/bin/activate
nohup {python} {' '.join(args)} > /tmp/subprotox.log 2>&1 &
'''

        script_path = '/tmp/subprotox_restart.sh'
        with open(script_path, 'w') as f:
            f.write(restart_script)
        os.chmod(script_path, 0o755)

        # Start the restart script in background
        subprocess.Popen(['/bin/bash', script_path],
                        start_new_session=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)

        # Give script time to start
        time.sleep(0.5)

        # Terminate current process
        os.kill(pid, signal.SIGTERM)

    # Start restart in background thread
    thread = threading.Thread(target=restart)
    thread.daemon = True
    thread.start()

    return jsonify({'success': True, 'message': 'Service is restarting...'})


@management_bp.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('static', filename)


@management_bp.route('/api/github/info', methods=['GET'])
def get_github_info():
    """Get GitHub repository information"""
    github_api = current_app.config.get('GITHUB_API')
    if not github_api:
        return jsonify({'error': 'GitHub integration not enabled'}), 400

    owner = request.args.get('owner', 'user')
    repo = request.args.get('repo', 'SubProtoX')

    repo_info = github_api.get_repo_info(owner, repo)
    if repo_info:
        return jsonify({
            'name': repo_info.get('name'),
            'full_name': repo_info.get('full_name'),
            'description': repo_info.get('description'),
            'html_url': repo_info.get('html_url'),
            'stargazers_count': repo_info.get('stargazers_count'),
            'forks_count': repo_info.get('forks_count'),
            'language': repo_info.get('language'),
            'updated_at': repo_info.get('updated_at')
        })
    else:
        return jsonify({'error': 'Failed to fetch repository information'}), 500


@management_bp.route('/api/github/releases/latest', methods=['GET'])
def get_latest_release():
    """Get latest release information"""
    github_api = current_app.config.get('GITHUB_API')
    if not github_api:
        return jsonify({'error': 'GitHub integration not enabled'}), 400

    owner = request.args.get('owner', 'user')
    repo = request.args.get('repo', 'SubProtoX')

    release_info = github_api.get_latest_release(owner, repo)
    if release_info:
        return jsonify({
            'tag_name': release_info.get('tag_name'),
            'name': release_info.get('name'),
            'body': release_info.get('body'),
            'published_at': release_info.get('published_at'),
            'html_url': release_info.get('html_url'),
            'download_url': release_info.get('zipball_url')
        })
    else:
        return jsonify({'error': 'Failed to fetch release information'}), 500
