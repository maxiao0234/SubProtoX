#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SubProtoX Configuration Template
Copy this file to config.py and modify the settings according to your environment
"""

import os

# Server configuration
SERVER_CONFIG = {
    'host': '0.0.0.0',
    'port': 7777,
    'debug': False,
    'base_path': ''  # Panel URL base path (e.g., 'subprotox' becomes '/subprotox/'), empty for root path
}

# SSL configuration
SSL_CONFIG = {
    'enabled': False,  # Enable HTTPS
    'cert_path': '',  # SSL certificate path
    'key_path': '',   # SSL private key path
    'domain': ''      # Custom domain (optional)
}

# Database configuration
DATABASE_CONFIG = {
    'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gringotts.db')
}

# Rules directory configuration
RULES_CONFIG = {
    'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rules')
}

# Default user configuration (Please change the default password!)
DEFAULT_USER = {
    'username': 'admin',
    'password': 'admin'  # ⚠️ Please change this password immediately after deployment!
}

# Security configuration
SECURITY_CONFIG = {
    'secret_key': None,  # Will generate random key if None
    'session_timeout': 24 * 60 * 60  # Session timeout in seconds
}

# Subscription conversion configuration
CONVERTER_CONFIG = {
    'max_proxies': 1000,  # Maximum number of proxies limit
    'timeout': 30,  # Subscription fetch timeout in seconds
    'user_agent': 'SubProtoX/1.0'
}

# Logging configuration
LOG_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': None  # Log file path, None means output to console
}

def get_config():
    """Get configuration dictionary"""
    return {
        'server': SERVER_CONFIG,
        'ssl': SSL_CONFIG,
        'database': DATABASE_CONFIG,
        'rules': RULES_CONFIG,
        'default_user': DEFAULT_USER,
        'security': SECURITY_CONFIG,
        'converter': CONVERTER_CONFIG,
        'log': LOG_CONFIG
    }

def validate_config():
    """Validate configuration settings"""
    errors = []

    # Check port range
    if not (1 <= SERVER_CONFIG['port'] <= 65535):
        errors.append(f"Invalid port number: {SERVER_CONFIG['port']}")

    # Check database directory permissions
    db_dir = os.path.dirname(DATABASE_CONFIG['path'])
    if not os.access(db_dir, os.W_OK):
        errors.append(f"Database directory has no write permission: {db_dir}")

    return errors

if __name__ == '__main__':
    # Validate configuration
    errors = validate_config()
    if errors:
        print("Configuration validation failed:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("Configuration validation passed")

    # Print current configuration
    import json
    config = get_config()
    print("\nCurrent configuration:")
    print(json.dumps(config, indent=2, ensure_ascii=False))