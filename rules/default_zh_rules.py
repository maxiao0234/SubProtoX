#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Default Rules with Chinese Interface
Balanced routing rules suitable for general use
"""

from typing import List
from .base_rules import BaseRuleSet


class DefaultZhRuleSet(BaseRuleSet):
    """Default routing rules with Chinese interface"""

    def __init__(self):
        super().__init__(
            name="Default Routing (Chinese Interface)",
            description="Template of balanced routing rules with Chinese interface"
        )

    def get_rules(self) -> List[str]:
        """Get balanced routing rules"""
        return [
            # Local network addresses
            'DOMAIN-SUFFIX,local,🎯 全球直连',
            'IP-CIDR,127.0.0.0/8,🎯 全球直连,no-resolve',
            'IP-CIDR,192.168.0.0/16,🎯 全球直连,no-resolve',
            'IP-CIDR,10.0.0.0/8,🎯 全球直连,no-resolve',
            'IP-CIDR,172.16.0.0/12,🎯 全球直连,no-resolve',

            # Cloud service providers
            'DOMAIN-SUFFIX,aliyun.com,🎯 全球直连',
            'DOMAIN-SUFFIX,tencent.com,🎯 全球直连',
            'DOMAIN-SUFFIX,qcloud.com,🎯 全球直连',
            'DOMAIN-SUFFIX,huaweicloud.com,🎯 全球直连',

            # Telegram
            'DOMAIN-SUFFIX,t.me,📲 资讯平台',
            'DOMAIN-SUFFIX,telegram.org,📲 资讯平台',
            'IP-CIDR,91.108.0.0/16,📲 资讯平台,no-resolve',
            'IP-CIDR,109.239.140.0/24,📲 资讯平台,no-resolve',
            'IP-CIDR,149.154.160.0/20,📲 资讯平台,no-resolve',

            # International streaming platforms
            'DOMAIN-SUFFIX,youtube.com,🌍 全球媒体',
            'DOMAIN-SUFFIX,googlevideo.com,🌍 全球媒体',
            'DOMAIN-SUFFIX,ytimg.com,🌍 全球媒体',
            'DOMAIN-SUFFIX,netflix.com,🌍 全球媒体',
            'DOMAIN-SUFFIX,nflxvideo.net,🌍 全球媒体',
            'DOMAIN-SUFFIX,twitch.tv,🌍 全球媒体',
            'DOMAIN-SUFFIX,hbo.com,🌍 全球媒体',
            'DOMAIN-SUFFIX,hbomax.com,🌍 全球媒体',
            'DOMAIN-SUFFIX,disney.com,🌍 全球媒体',
            'DOMAIN-SUFFIX,disneyplus.com,🌍 全球媒体',

            # Gaming platforms
            'DOMAIN-SUFFIX,steam.com,🎮 游戏平台',
            'DOMAIN-SUFFIX,steamcommunity.com,🎮 游戏平台',
            'DOMAIN-SUFFIX,steampowered.com,🎮 游戏平台',
            'DOMAIN-SUFFIX,epicgames.com,🎮 游戏平台',
            'DOMAIN-SUFFIX,origin.com,🎮 游戏平台',
            'DOMAIN-SUFFIX,ea.com,🎮 游戏平台',
            'DOMAIN-SUFFIX,blizzard.com,🎮 游戏平台',
            'DOMAIN-SUFFIX,battle.net,🎮 游戏平台',

            # Popular international services
            'DOMAIN-SUFFIX,google.com,🚀 节点选择',
            'DOMAIN-SUFFIX,github.com,🚀 节点选择',
            'DOMAIN-SUFFIX,twitter.com,🚀 节点选择',
            'DOMAIN-SUFFIX,facebook.com,🚀 节点选择',
            'DOMAIN-SUFFIX,instagram.com,🚀 节点选择',

            # Domestic domains
            'DOMAIN-SUFFIX,cn,🎯 全球直连',
            'DOMAIN-SUFFIX,baidu.com,🎯 全球直连',
            'DOMAIN-SUFFIX,qq.com,🎯 全球直连',
            'DOMAIN-SUFFIX,taobao.com,🎯 全球直连',
            'DOMAIN-SUFFIX,jd.com,🎯 全球直连',
            'DOMAIN-SUFFIX,bilibili.com,🎯 全球直连',
            'DOMAIN-SUFFIX,weibo.com,🎯 全球直连',
            'DOMAIN-SUFFIX,zhihu.com,🎯 全球直连',
            'DOMAIN-SUFFIX,douban.com,🎯 全球直连',
            'DOMAIN-SUFFIX,sina.com.cn,🎯 全球直连',

            # Advertisement blocking
            'DOMAIN-KEYWORD,admarvel,🛑 全球拦截',
            'DOMAIN-KEYWORD,admaster,🛑 全球拦截',
            'DOMAIN-KEYWORD,adsage,🛑 全球拦截',
            'DOMAIN-KEYWORD,adsensor,🛑 全球拦截',
            'DOMAIN-KEYWORD,adservice,🛑 全球拦截',
            'DOMAIN-KEYWORD,adwords,🛑 全球拦截',
            'DOMAIN-KEYWORD,analytics,🛑 全球拦截',
            'DOMAIN-KEYWORD,clickserve,🛑 全球拦截',

            # GeoIP routing
            'GEOIP,CN,🎯 全球直连',

            # Final catch-all rule
            'MATCH,🐟 漏网之鱼'
        ]