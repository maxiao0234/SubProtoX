#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SubProtoX Rules Module
This module contains all routing rules and proxy group configurations
"""

from .rule_manager import RuleManager
from .base_rules import BaseRuleSet
from .default_zh_rules import DefaultZhRuleSet
from .default_rules import DefaultRuleSet
from .research_rules import ResearchRuleSet
from .minimal_rules import MinimalRuleSet
from .proxy_groups import ProxyGroupGenerator

__all__ = [
    'RuleManager',
    'BaseRuleSet',
    'DefaultZhRuleSet',
    'DefaultRuleSet',
    'ResearchRuleSet',
    'MinimalRuleSet',
    'ProxyGroupGenerator'
]