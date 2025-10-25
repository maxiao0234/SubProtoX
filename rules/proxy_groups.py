#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Proxy Group Generator
Generates proxy groups for Clash configuration
"""

from typing import List, Dict, Any


class ProxyGroupGenerator:
    """Generate proxy groups for Clash configuration"""

    @staticmethod
    def generate_proxy_groups(proxy_names: List[str]) -> List[Dict[str, Any]]:
        """Generate proxy groups (fix circular dependency)"""
        if not proxy_names:
            proxy_names = ['DIRECT']

        return [
            {
                'name': '🚀 节点选择',
                'type': 'select',
                'proxies': ['♻️ 自动选择', 'DIRECT'] + proxy_names
            },
            {
                'name': '♻️ 自动选择',
                'type': 'url-test',
                'proxies': proxy_names,
                'url': 'http://www.gstatic.com/generate_204',
                'interval': 300,
                'tolerance': 50
            },
            {
                'name': '🌍 全球媒体',
                'type': 'select',
                'proxies': ['🚀 节点选择', '♻️ 自动选择', 'DIRECT']
            },
            {
                'name': '📲 资讯平台',
                'type': 'select',
                'proxies': ['🚀 节点选择', '♻️ 自动选择']
            },
            {
                'name': '🎮 游戏平台',
                'type': 'select',
                'proxies': ['🚀 节点选择', 'DIRECT', '♻️ 自动选择']
            },
            {
                'name': '🎯 全球直连',
                'type': 'select',
                'proxies': ['DIRECT']  # 移除了可能造成循环的 '🚀 节点选择'
            },
            {
                'name': '🛑 全球拦截',
                'type': 'select',
                'proxies': ['REJECT', 'DIRECT']
            },
            {
                'name': '🐟 漏网之鱼',
                'type': 'select',
                'proxies': ['🚀 节点选择', 'DIRECT', '♻️ 自动选择']
            }
        ]

    @staticmethod
    def generate_research_proxy_groups(proxy_names: List[str]) -> List[Dict[str, Any]]:
        """Generate research-optimized proxy groups"""
        if not proxy_names:
            proxy_names = ['DIRECT']

        return [
            {
                'name': '🚀 Proxy',
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
            },
            {
                'name': '🤖 AI Research',
                'type': 'select',
                'proxies': ['🚀 Proxy', '♻️ Auto Select']
            },
            {
                'name': '💻 Development',
                'type': 'select',
                'proxies': ['🚀 Proxy', '♻️ Auto Select']
            },
            {
                'name': '📚 Academic',
                'type': 'select',
                'proxies': ['🚀 Proxy', '♻️ Auto Select']
            },
            {
                'name': '☁️ Cloud',
                'type': 'select',
                'proxies': ['🚀 Proxy', 'DIRECT', '♻️ Auto Select']
            },
            {
                'name': '📖 Knowledge',
                'type': 'select',
                'proxies': ['🚀 Proxy', 'DIRECT']
            },
            {
                'name': '🛑 Ad Block',
                'type': 'select',
                'proxies': ['REJECT', 'DIRECT']
            }
        ]

    @staticmethod
    def generate_minimal_proxy_groups(proxy_names: List[str]) -> List[Dict[str, Any]]:
        """Generate minimal proxy groups"""
        if not proxy_names:
            proxy_names = ['DIRECT']

        return [
            {
                'name': '🚀 Proxy',
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