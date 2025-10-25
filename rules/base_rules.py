#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Base RuleSet class for all rule implementations
"""

from abc import ABC, abstractmethod
from typing import List


class BaseRuleSet(ABC):
    """Base class for all rule sets"""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description

    @abstractmethod
    def get_rules(self) -> List[str]:
        """
        Return list of routing rules
        Each rule should be in format: "TYPE,PATTERN,POLICY"
        """
        pass

    def get_info(self) -> dict:
        """Get rule set information"""
        return {
            'name': self.name,
            'description': self.description,
            'rule_count': len(self.get_rules())
        }