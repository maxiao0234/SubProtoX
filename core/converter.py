#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SubProtoX Core Converter Module
Contains the main conversion logic for VPN protocols
"""

import os
import json
import yaml
import base64
import hashlib
import sqlite3
import urllib.parse
from datetime import datetime
from typing import Optional, List, Dict, Any


class SubConverter:
    """Main converter class for VPN subscription and protocol conversion"""

    def __init__(self, db_path: str, rules_path: str, default_username: str,
                 default_password: str, rule_manager=None):
        """
        Initialize SubConverter

        Args:
            db_path: Path to SQLite database
            rules_path: Path to rules directory
            default_username: Default admin username
            default_password: Default admin password
            rule_manager: Optional RuleManager instance
        """
        self.db_path = db_path
        self.rules_path = rules_path
        self.default_username = default_username
        self.default_password = default_password
        self.rule_manager = rule_manager

        self.init_db()

        # Initialize rule manager or use fallback
        if self.rule_manager:
            self.rule_manager.initialize_default_rules_in_db()
        else:
            self.init_default_rules()

    def init_db(self):
        """Initialize database"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Create conversion records table (added proxies_count field)
        c.execute('''
            CREATE TABLE IF NOT EXISTS conversions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                token TEXT UNIQUE NOT NULL,
                config TEXT NOT NULL,
                proxies_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create rules table
        c.execute('''
            CREATE TABLE IF NOT EXISTS rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create users table
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create runtime_config table for hot-reload settings
        c.execute('''
            CREATE TABLE IF NOT EXISTS runtime_config (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Add default user
        password_hash = hashlib.sha256(self.default_password.encode()).hexdigest()
        c.execute(
            'INSERT OR IGNORE INTO users (username, password_hash) VALUES (?, ?)',
            (self.default_username, password_hash)
        )

        conn.commit()
        conn.close()

    def init_default_rules(self):
        """Initialize default rules (fallback when rules module is not available)"""
        os.makedirs(self.rules_path, exist_ok=True)

        # Default rule sets
        default_rules = {
            'china': self.get_china_rules(),
            'global': self.get_global_rules(),
            'research': self.get_research_rules(),
            'minimal': self.get_minimal_rules()
        }

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        for name, content in default_rules.items():
            c.execute(
                'INSERT OR IGNORE INTO rules (name, description, content) VALUES (?, ?, ?)',
                (name, f'{name.title()} rule set', '\n'.join(content))
            )

        conn.commit()
        conn.close()

    def parse_vless(self, url: str) -> Optional[Dict[str, Any]]:
        """Parse Vless link"""
        try:
            # Handle special characters in URL
            if '#' in url:
                url, fragment = url.split('#', 1)
                fragment = urllib.parse.unquote(fragment)
            else:
                fragment = None

            parsed = urllib.parse.urlparse(url)
            uuid = parsed.username
            server = parsed.hostname
            port = parsed.port or 443
            params = urllib.parse.parse_qs(parsed.query)

            # Get node name
            name = fragment if fragment else params.get('remarks', [f'vless-{server}'])[0] if 'remarks' in params else f'vless-{server}'

            proxy = {
                'name': name,
                'type': 'vless',
                'server': server,
                'port': port,
                'uuid': uuid,
                'udp': True,
                'skip-cert-verify': True
            }

            # Handle transport protocol
            network = params.get('type', ['tcp'])[0]
            if network == 'ws':
                proxy['network'] = 'ws'
                proxy['ws-opts'] = {
                    'path': params.get('path', ['/'])[0],
                    'headers': {'Host': params.get('host', [server])[0]}
                }
            elif network == 'grpc':
                proxy['network'] = 'grpc'
                proxy['grpc-opts'] = {
                    'grpc-service-name': params.get('serviceName', [''])[0]
                }

            # Handle TLS
            if params.get('security', [''])[0] == 'tls':
                proxy['tls'] = True
                if 'sni' in params:
                    proxy['servername'] = params['sni'][0]

            # Handle flow (TCP/TLS only)
            if network == 'tcp' and 'flow' in params:
                proxy['flow'] = params['flow'][0]

            return proxy
        except Exception as e:
            print(f"Error parsing vless: {e} - URL: {url}")
            return None

    def parse_vmess(self, url: str) -> Optional[Dict[str, Any]]:
        """Parse Vmess link"""
        try:
            # Remove vmess:// prefix and decode
            data = base64.b64decode(url.replace('vmess://', '')).decode('utf-8')
            vmess = json.loads(data)

            proxy = {
                'name': vmess.get('ps', f"vmess-{vmess.get('add')}"),
                'type': 'vmess',
                'server': vmess.get('add'),
                'port': int(vmess.get('port', 443)),
                'uuid': vmess.get('id'),
                'alterId': int(vmess.get('aid', 0)),
                'cipher': vmess.get('scy', 'auto'),
                'skip-cert-verify': True
            }

            # Handle transport protocol
            network = vmess.get('net', 'tcp')
            if network == 'ws':
                proxy['network'] = 'ws'
                proxy['ws-opts'] = {
                    'path': vmess.get('path', '/'),
                    'headers': {'Host': vmess.get('host', vmess.get('add'))}
                }

            return proxy
        except Exception as e:
            print(f"Error parsing vmess: {e}")
            return None

    def parse_trojan(self, url: str) -> Optional[Dict[str, Any]]:
        """Parse Trojan link"""
        try:
            parsed = urllib.parse.urlparse(url)
            password = parsed.username
            server = parsed.hostname
            port = parsed.port
            params = urllib.parse.parse_qs(parsed.query)

            proxy = {
                'name': params.get('remarks', [f'trojan-{server}'])[0],
                'type': 'trojan',
                'server': server,
                'port': port,
                'password': password,
                'skip-cert-verify': True
            }

            if 'sni' in params:
                proxy['sni'] = params['sni'][0]

            return proxy
        except Exception as e:
            print(f"Error parsing trojan: {e}")
            return None

    def parse_shadowsocks(self, url: str) -> Optional[Dict[str, Any]]:
        """Parse Shadowsocks link"""
        try:
            # Remove ss:// prefix
            data = url.replace('ss://', '')

            # Handle format with @
            if '@' in data:
                auth, server_info = data.split('@')
                auth = base64.b64decode(auth + '=' * (4 - len(auth) % 4)).decode('utf-8')
                method, password = auth.split(':')
                server, port = server_info.split(':')
                port = int(port.split('#')[0])

                proxy = {
                    'name': f'ss-{server}',
                    'type': 'ss',
                    'server': server,
                    'port': port,
                    'cipher': method,
                    'password': password
                }

                return proxy
        except Exception as e:
            print(f"Error parsing shadowsocks: {e}")
            return None

    def parse_link(self, link: str) -> Optional[Dict[str, Any]]:
        """Parse various types of proxy links"""
        link = link.strip()

        if link.startswith('vless://'):
            return self.parse_vless(link)
        elif link.startswith('vmess://'):
            return self.parse_vmess(link)
        elif link.startswith('trojan://'):
            return self.parse_trojan(link)
        elif link.startswith('ss://'):
            return self.parse_shadowsocks(link)

        return None

    def generate_clash_config(self, proxies: List[Dict[str, Any]],
                            rule_name: str = 'default') -> str:
        """Generate Clash configuration"""
        # Get rules
        if self.rule_manager:
            rules = self.rule_manager.get_rules_by_name(rule_name)
            proxy_groups = self.rule_manager.get_proxy_groups([p['name'] for p in proxies], rule_name)
        else:
            # Fallback to old method
            rules = self.get_rules_by_name(rule_name)
            proxy_groups = self.generate_proxy_groups([p['name'] for p in proxies])

        # Basic configuration
        config = {
            'port': 7890,
            'socks-port': 7891,
            'mixed-port': 7892,
            'allow-lan': True,
            'mode': 'rule',
            'log-level': 'info',
            'external-controller': '127.0.0.1:9090',
            'dns': {
                'enable': True,
                'enhanced-mode': 'fake-ip',
                'fake-ip-range': '198.18.0.1/16',
                'nameserver': [
                    '223.5.5.5',
                    '114.114.114.114',
                    '8.8.8.8'
                ],
                'fallback': [
                    '1.1.1.1',
                    '8.8.4.4'
                ]
            },
            'proxies': proxies,
            'proxy-groups': proxy_groups,
            'rules': rules
        }

        return yaml.dump(config, allow_unicode=True, default_flow_style=False, sort_keys=False)

    def get_china_rules(self) -> List[str]:
        """Get China mainland optimized rules (fallback)"""
        return [
            'DOMAIN-SUFFIX,local,DIRECT',
            'IP-CIDR,127.0.0.0/8,DIRECT,no-resolve',
            'IP-CIDR,192.168.0.0/16,DIRECT,no-resolve',
            'IP-CIDR,10.0.0.0/8,DIRECT,no-resolve',
            'GEOIP,CN,DIRECT',
            'MATCH,🚀 Node Selection'
        ]

    def get_global_rules(self) -> List[str]:
        """Get global optimized rules (fallback)"""
        return [
            'DOMAIN-SUFFIX,local,DIRECT',
            'IP-CIDR,127.0.0.0/8,DIRECT,no-resolve',
            'IP-CIDR,192.168.0.0/16,DIRECT,no-resolve',
            'IP-CIDR,10.0.0.0/8,DIRECT,no-resolve',
            'MATCH,🚀 Node Selection'
        ]

    def get_research_rules(self) -> List[str]:
        """Get academic/research optimized rules (fallback)"""
        return [
            'DOMAIN-SUFFIX,local,DIRECT',
            'IP-CIDR,127.0.0.0/8,DIRECT,no-resolve',
            'IP-CIDR,192.168.0.0/16,DIRECT,no-resolve',
            'IP-CIDR,10.0.0.0/8,DIRECT,no-resolve',
            'MATCH,🚀 Node Selection'
        ]

    def get_minimal_rules(self) -> List[str]:
        """Get minimal rule set (fallback)"""
        return [
            'DOMAIN-SUFFIX,local,DIRECT',
            'IP-CIDR,127.0.0.0/8,DIRECT,no-resolve',
            'IP-CIDR,192.168.0.0/16,DIRECT,no-resolve',
            'IP-CIDR,10.0.0.0/8,DIRECT,no-resolve',
            'GEOIP,CN,DIRECT',
            'MATCH,🚀 Node Selection'
        ]

    def generate_proxy_groups(self, proxy_names: List[str]) -> List[Dict[str, Any]]:
        """Generate proxy groups (fallback)"""
        if not proxy_names:
            proxy_names = ['DIRECT']

        return [
            {
                'name': '🚀 Node Selection',
                'type': 'select',
                'proxies': ['♻️ Auto Select', 'DIRECT'] + proxy_names
            },
            {
                'name': '♻️ Auto Select',
                'type': 'url-test',
                'proxies': proxy_names,
                'url': 'http://www.gstatic.com/generate_204',
                'interval': 300,
                'tolerance': 50
            }
        ]

    def get_rules_by_name(self, name: str) -> List[str]:
        """Get rules by name"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT content FROM rules WHERE name = ?', (name,))
        result = c.fetchone()
        conn.close()

        if result:
            return result[0].split('\n')
        return self.get_china_rules()

    def save_conversion(self, config: str, proxies_count: int = 0,
                       config_name: Optional[str] = None,
                       auto_update: bool = True,
                       update_interval_hours: int = 24,
                       traffic_limit_gb: int = 0) -> str:
        """Save conversion result with subscription settings"""
        token = hashlib.md5(f"{config}{datetime.now()}".encode()).hexdigest()[:16]

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Add new fields to database (if not exists)
        c.execute("PRAGMA table_info(conversions)")
        columns = [column[1] for column in c.fetchall()]
        if 'config_name' not in columns:
            c.execute('ALTER TABLE conversions ADD COLUMN config_name TEXT DEFAULT NULL')
        if 'auto_update' not in columns:
            c.execute('ALTER TABLE conversions ADD COLUMN auto_update INTEGER DEFAULT 1')
        if 'update_interval_hours' not in columns:
            c.execute('ALTER TABLE conversions ADD COLUMN update_interval_hours INTEGER DEFAULT 24')
        if 'traffic_limit_gb' not in columns:
            c.execute('ALTER TABLE conversions ADD COLUMN traffic_limit_gb INTEGER DEFAULT 0')

        c.execute(
            '''INSERT INTO conversions
               (token, config, proxies_count, config_name, auto_update, update_interval_hours, traffic_limit_gb)
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (token, config, proxies_count, config_name or f'config_{token}',
             1 if auto_update else 0, update_interval_hours, traffic_limit_gb)
        )
        conn.commit()
        conn.close()

        return token

    def get_conversion_with_settings(self, token: str) -> tuple:
        """Get conversion result with all subscription settings"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Check if new columns exist
        c.execute("PRAGMA table_info(conversions)")
        columns = [column[1] for column in c.fetchall()]

        if 'auto_update' in columns and 'update_interval_hours' in columns and 'traffic_limit_gb' in columns:
            c.execute('''SELECT config, config_name, auto_update, update_interval_hours, traffic_limit_gb
                        FROM conversions WHERE token = ?''', (token,))
            result = c.fetchone()
            conn.close()

            if result:
                return result[0], result[1] or f'config_{token}', bool(result[2]), result[3], result[4]
        else:
            # Fallback for old database structure
            c.execute('SELECT config, config_name FROM conversions WHERE token = ?', (token,))
            result = c.fetchone()
            conn.close()

            if result:
                return result[0], result[1] or f'config_{token}', True, 24, 0

        return None, None, True, 24, 0

    def get_conversion_with_name(self, token: str) -> tuple:
        """Get conversion result and configuration name (backward compatibility)"""
        config, name, _, _, _ = self.get_conversion_with_settings(token)
        return config, name

    def get_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get history records"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            'SELECT token, proxies_count, created_at FROM conversions ORDER BY created_at DESC LIMIT ?',
            (limit,)
        )
        history = []
        for row in c.fetchall():
            history.append({
                'token': row[0],
                'proxies_count': row[1],
                'created_at': row[2]
            })
        conn.close()
        return history

    def delete_conversion(self, token: str):
        """Delete conversion record"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('DELETE FROM conversions WHERE token = ?', (token,))
        conn.commit()
        conn.close()

    def clear_all_history(self):
        """Clear all history records"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('DELETE FROM conversions')
        conn.commit()
        conn.close()

    def verify_user(self, username: str, password: str) -> bool:
        """Verify user credentials"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        c.execute(
            'SELECT id FROM users WHERE username = ? AND password_hash = ?',
            (username, password_hash)
        )
        result = c.fetchone()
        conn.close()
        return result is not None

    def change_account(self, username: str, new_username: Optional[str] = None,
                      new_password: Optional[str] = None) -> bool:
        """Change account information"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        try:
            # Use transaction to ensure atomicity
            c.execute('BEGIN TRANSACTION')

            # Update both username and password in a single operation if both are provided
            if new_username and new_password:
                password_hash = hashlib.sha256(new_password.encode()).hexdigest()
                c.execute(
                    'UPDATE users SET username = ?, password_hash = ? WHERE username = ?',
                    (new_username, password_hash, username)
                )
            elif new_username:
                # Only update username
                c.execute(
                    'UPDATE users SET username = ? WHERE username = ?',
                    (new_username, username)
                )
            elif new_password:
                # Only update password
                password_hash = hashlib.sha256(new_password.encode()).hexdigest()
                c.execute(
                    'UPDATE users SET password_hash = ? WHERE username = ?',
                    (password_hash, username)
                )

            # Check if any row was affected
            if c.rowcount == 0:
                conn.rollback()
                conn.close()
                return False

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.rollback()
            conn.close()
            print(f"Error updating account: {e}")
            return False

    def get_runtime_config(self, key: str, default: Any = None) -> Any:
        """Get runtime configuration value from database"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT value FROM runtime_config WHERE key = ?', (key,))
        result = c.fetchone()
        conn.close()

        if result is None:
            return default

        # Try to parse JSON value
        try:
            return json.loads(result[0])
        except (json.JSONDecodeError, TypeError):
            return result[0]

    def set_runtime_config(self, key: str, value: Any) -> bool:
        """Set runtime configuration value in database"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        try:
            # Convert value to JSON string for storage
            if isinstance(value, (dict, list)):
                json_value = json.dumps(value)
            else:
                json_value = str(value) if value is not None else None

            c.execute('''
                INSERT OR REPLACE INTO runtime_config (key, value, updated_at)
                VALUES (?, ?, datetime('now'))
            ''', (key, json_value))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.rollback()
            conn.close()
            print(f"Error setting runtime config: {e}")
            return False
