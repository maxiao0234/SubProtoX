#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Rule Manager - Manages all routing rules and provides unified interface
"""

import sqlite3
from typing import List, Dict, Optional
from .base_rules import BaseRuleSet
from .default_zh_rules import DefaultZhRuleSet
from .default_rules import DefaultRuleSet
from .research_rules import ResearchRuleSet
from .minimal_rules import MinimalRuleSet
from .proxy_groups import ProxyGroupGenerator


class RuleManager:
    """Manages all routing rules and provides unified interface"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.built_in_rules = {
            'Default Routing (Chinese Interface)': DefaultZhRuleSet(),
            'Default Routing': DefaultRuleSet(),
            'Academic & Research Routing': ResearchRuleSet(),
            'Minimal Rules': MinimalRuleSet()
        }
        self.proxy_group_generator = ProxyGroupGenerator()

    def get_rules_by_name(self, rule_name: str) -> List[str]:
        """
        Get rules by name
        First check built-in rules, then check database
        """
        # Check built-in rules first
        if rule_name in self.built_in_rules:
            return self.built_in_rules[rule_name].get_rules()

        # Check database for custom rules
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute('SELECT content FROM rules WHERE name = ?', (rule_name,))
            result = c.fetchone()
            conn.close()

            if result:
                return result[0].split('\n')
        except Exception as e:
            print(f"Error getting rules from database: {e}")

        # Return Default Routing (Chinese Interface) rules as fallback
        return self.built_in_rules['Default Routing (Chinese Interface)'].get_rules()

    def get_proxy_groups(self, proxy_names: List[str], rule_name: str = 'Default Routing (Chinese Interface)') -> List[Dict]:
        """Get proxy groups based on rule name"""
        if rule_name == 'Academic & Research Routing':
            return self.proxy_group_generator.generate_research_proxy_groups(proxy_names)
        elif rule_name == 'Minimal Rules':
            return self.proxy_group_generator.generate_minimal_proxy_groups(proxy_names)
        else:
            return self.proxy_group_generator.generate_proxy_groups(proxy_names)

    def list_built_in_rules(self) -> Dict[str, str]:
        """List all built-in rule sets"""
        return {
            name: rule_set.description
            for name, rule_set in self.built_in_rules.items()
        }

    def get_rule_info(self, rule_name: str) -> Optional[Dict]:
        """Get information about a specific rule"""
        if rule_name in self.built_in_rules:
            return self.built_in_rules[rule_name].get_info()

        # Check database for custom rules
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute('SELECT name, description, content FROM rules WHERE name = ?', (rule_name,))
            result = c.fetchone()
            conn.close()

            if result:
                return {
                    'name': result[0],
                    'description': result[1] or 'Custom rule',
                    'rule_count': len(result[2].split('\n'))
                }
        except Exception as e:
            print(f"Error getting rule info from database: {e}")

        return None

    def initialize_default_rules_in_db(self):
        """Initialize default rules in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()

            for name, rule_set in self.built_in_rules.items():
                rules_content = '\n'.join(rule_set.get_rules())
                c.execute(
                    'INSERT OR IGNORE INTO rules (name, description, content) VALUES (?, ?, ?)',
                    (name, rule_set.description, rules_content)
                )

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error initializing default rules in database: {e}")