#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Default English Interface Rules - Optimized for international users
"""

from typing import List
from .base_rules import BaseRuleSet


class DefaultRuleSet(BaseRuleSet):
    """Default balanced routing rules"""

    def __init__(self):
        super().__init__(
            name="Default Routing",
            description="Template of default balanced routing rules"
        )

    def get_rules(self) -> List[str]:
        """Get global optimized rules"""
        return [
            # Local addresses
            'DOMAIN-SUFFIX,local,DIRECT',
            'IP-CIDR,127.0.0.0/8,DIRECT,no-resolve',
            'IP-CIDR,192.168.0.0/16,DIRECT,no-resolve',
            'IP-CIDR,10.0.0.0/8,DIRECT,no-resolve',
            'IP-CIDR,172.16.0.0/12,DIRECT,no-resolve',

            # Streaming services
            'DOMAIN-SUFFIX,youtube.com,🌍 Streaming',
            'DOMAIN-SUFFIX,googlevideo.com,🌍 Streaming',
            'DOMAIN-SUFFIX,netflix.com,🌍 Streaming',
            'DOMAIN-SUFFIX,nflxvideo.net,🌍 Streaming',
            'DOMAIN-SUFFIX,hulu.com,🌍 Streaming',
            'DOMAIN-SUFFIX,amazon.com,🌍 Streaming',
            'DOMAIN-SUFFIX,primevideo.com,🌍 Streaming',
            'DOMAIN-SUFFIX,disneyplus.com,🌍 Streaming',

            # Social media
            'DOMAIN-SUFFIX,facebook.com,📱 Social',
            'DOMAIN-SUFFIX,instagram.com,📱 Social',
            'DOMAIN-SUFFIX,twitter.com,📱 Social',
            'DOMAIN-SUFFIX,tiktok.com,📱 Social',
            'DOMAIN-SUFFIX,snapchat.com,📱 Social',
            'DOMAIN-SUFFIX,linkedin.com,📱 Social',

            # Gaming
            'DOMAIN-SUFFIX,steam.com,🎮 Gaming',
            'DOMAIN-SUFFIX,epicgames.com,🎮 Gaming',
            'DOMAIN-SUFFIX,blizzard.com,🎮 Gaming',
            'DOMAIN-SUFFIX,ea.com,🎮 Gaming',
            'DOMAIN-SUFFIX,ubisoft.com,🎮 Gaming',

            # News and information
            'DOMAIN-SUFFIX,bbc.com,📰 News',
            'DOMAIN-SUFFIX,cnn.com,📰 News',
            'DOMAIN-SUFFIX,nytimes.com,📰 News',
            'DOMAIN-SUFFIX,reuters.com,📰 News',
            'DOMAIN-SUFFIX,wsj.com,📰 News',

            # Ad blocking
            'DOMAIN-KEYWORD,advertisement,🛑 Ad Block',
            'DOMAIN-KEYWORD,analytics,🛑 Ad Block',
            'DOMAIN-KEYWORD,tracking,🛑 Ad Block',

            # Final rule
            'MATCH,🚀 Proxy'
        ]