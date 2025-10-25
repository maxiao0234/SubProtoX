#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Research Rules - Optimized for academic research scenarios
"""

from typing import List
from .base_rules import BaseRuleSet


class ResearchRuleSet(BaseRuleSet):
    """Academic research optimized rules"""

    def __init__(self):
        super().__init__(
            name="Academic & Research Routing",
            description="Academic and research resource optimized routing rules"
        )

    def get_rules(self) -> List[str]:
        """Get academic/research optimized rules"""
        return [
            # Local addresses
            'DOMAIN-SUFFIX,local,DIRECT',
            'IP-CIDR,127.0.0.0/8,DIRECT,no-resolve',
            'IP-CIDR,192.168.0.0/16,DIRECT,no-resolve',
            'IP-CIDR,10.0.0.0/8,DIRECT,no-resolve',
            'IP-CIDR,172.16.0.0/12,DIRECT,no-resolve',

            # AI and ML platforms
            'DOMAIN-SUFFIX,openai.com,🤖 AI Research',
            'DOMAIN-SUFFIX,anthropic.com,🤖 AI Research',
            'DOMAIN-SUFFIX,claude.ai,🤖 AI Research',
            'DOMAIN-SUFFIX,gemini.google.com,🤖 AI Research',
            'DOMAIN-SUFFIX,ai.google.dev,🤖 AI Research',
            'DOMAIN-SUFFIX,bard.google.com,🤖 AI Research',
            'DOMAIN-SUFFIX,perplexity.ai,🤖 AI Research',
            'DOMAIN-SUFFIX,mistral.ai,🤖 AI Research',
            'DOMAIN-SUFFIX,huggingface.co,🤖 AI Research',
            'DOMAIN-SUFFIX,stability.ai,🤖 AI Research',
            'DOMAIN-SUFFIX,midjourney.com,🤖 AI Research',
            'DOMAIN-SUFFIX,runwayml.com,🤖 AI Research',
            'DOMAIN-SUFFIX,replicate.com,🤖 AI Research',
            'DOMAIN-SUFFIX,together.ai,🤖 AI Research',
            'DOMAIN-SUFFIX,pytorch.org,🤖 AI Research',
            'DOMAIN-SUFFIX,tensorflow.org,🤖 AI Research',
            'DOMAIN-SUFFIX,keras.io,🤖 AI Research',
            'DOMAIN-SUFFIX,paperswithcode.com,🤖 AI Research',
            'DOMAIN-SUFFIX,arxiv.org,🤖 AI Research',
            'DOMAIN-SUFFIX,deepmind.com,🤖 AI Research',
            'DOMAIN-SUFFIX,cohere.ai,🤖 AI Research',
            'DOMAIN-SUFFIX,scale.com,🤖 AI Research',

            # Code repositories and development
            'DOMAIN-SUFFIX,github.com,💻 Development',
            'DOMAIN-SUFFIX,gitlab.com,💻 Development',
            'DOMAIN-SUFFIX,bitbucket.org,💻 Development',
            'DOMAIN-SUFFIX,stackoverflow.com,💻 Development',
            'DOMAIN-SUFFIX,stackexchange.com,💻 Development',
            'DOMAIN-SUFFIX,npmjs.com,💻 Development',
            'DOMAIN-SUFFIX,pypi.org,💻 Development',
            'DOMAIN-SUFFIX,packagist.org,💻 Development',
            'DOMAIN-SUFFIX,crates.io,💻 Development',

            # Google services (research tools)
            'DOMAIN-SUFFIX,scholar.google.com,📚 Academic',
            'DOMAIN-SUFFIX,google.com,📚 Academic',
            'DOMAIN-SUFFIX,googleapis.com,📚 Academic',
            'DOMAIN-SUFFIX,googleusercontent.com,📚 Academic',
            'DOMAIN-SUFFIX,drive.google.com,📚 Academic',
            'DOMAIN-SUFFIX,docs.google.com,📚 Academic',
            'DOMAIN-SUFFIX,colab.research.google.com,📚 Academic',

            # Academic and research
            'DOMAIN-SUFFIX,ieee.org,📚 Academic',
            'DOMAIN-SUFFIX,acm.org,📚 Academic',
            'DOMAIN-SUFFIX,springer.com,📚 Academic',
            'DOMAIN-SUFFIX,nature.com,📚 Academic',
            'DOMAIN-SUFFIX,science.org,📚 Academic',
            'DOMAIN-SUFFIX,elsevier.com,📚 Academic',
            'DOMAIN-SUFFIX,wiley.com,📚 Academic',
            'DOMAIN-SUFFIX,pubmed.ncbi.nlm.nih.gov,📚 Academic',
            'DOMAIN-SUFFIX,researchgate.net,📚 Academic',
            'DOMAIN-SUFFIX,academia.edu,📚 Academic',

            # Cloud and compute platforms
            'DOMAIN-SUFFIX,amazonaws.com,☁️ Cloud',
            'DOMAIN-SUFFIX,azure.com,☁️ Cloud',
            'DOMAIN-SUFFIX,microsoftonline.com,☁️ Cloud',
            'DOMAIN-SUFFIX,googlecloud.com,☁️ Cloud',
            'DOMAIN-SUFFIX,digitalocean.com,☁️ Cloud',
            'DOMAIN-SUFFIX,heroku.com,☁️ Cloud',
            'DOMAIN-SUFFIX,netlify.com,☁️ Cloud',
            'DOMAIN-SUFFIX,vercel.com,☁️ Cloud',

            # Documentation and learning
            'DOMAIN-SUFFIX,wikipedia.org,📖 Knowledge',
            'DOMAIN-SUFFIX,wikimedia.org,📖 Knowledge',
            'DOMAIN-SUFFIX,mozilla.org,📖 Knowledge',
            'DOMAIN-SUFFIX,w3.org,📖 Knowledge',
            'DOMAIN-SUFFIX,mdn.mozilla.org,📖 Knowledge',

            # Ad blocking
            'DOMAIN-KEYWORD,analytics,🛑 Ad Block',
            'DOMAIN-KEYWORD,tracking,🛑 Ad Block',

            # Final rule
            'MATCH,🚀 Proxy'
        ]