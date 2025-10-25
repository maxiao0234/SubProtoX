#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Minimal Rules - Minimal rule set for simple configurations
"""

from typing import List
from .base_rules import BaseRuleSet


class MinimalRuleSet(BaseRuleSet):
    """Basic routing rule set"""

    def __init__(self):
        super().__init__(
            name="Minimal Rules",
            description="Basic routing rules with minimal configuration"
        )

    def get_rules(self) -> List[str]:
        """Get minimal rule set"""
        return [
            'DOMAIN-SUFFIX,local,DIRECT',
            'IP-CIDR,127.0.0.0/8,DIRECT,no-resolve',
            'IP-CIDR,192.168.0.0/16,DIRECT,no-resolve',
            'IP-CIDR,10.0.0.0/8,DIRECT,no-resolve',
            'IP-CIDR,172.16.0.0/12,DIRECT,no-resolve',
            'GEOIP,CN,DIRECT',
            'MATCH,🚀 Proxy'
        ]