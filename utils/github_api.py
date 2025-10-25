#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GitHub API Integration Module
Handles GitHub API requests with caching
"""

import time
import requests
from typing import Optional, Dict, Any


class GitHubAPI:
    """GitHub API integration with caching"""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize GitHub API client

        Args:
            config: Configuration dictionary containing github settings
        """
        self.config = config.get('github', {})
        self.cache_duration = self.config.get('cache_duration', 3600)
        self.timeout = self.config.get('timeout', 10)
        self.user_agent = config.get('converter', {}).get('user_agent', 'SubProtoX/1.0')
        self.cache = {}

    def _get_cache_key(self, endpoint: str) -> str:
        """Generate cache key for endpoint"""
        return f"github_{endpoint}"

    def _is_cache_valid(self, cache_data: Dict[str, Any]) -> bool:
        """Check if cached data is still valid"""
        return (time.time() - cache_data['timestamp']) < self.cache_duration

    def _make_request(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """Make request to GitHub API"""
        try:
            url = f"{self.config['api_url']}/{endpoint}"
            headers = {
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': self.user_agent
            }

            response = requests.get(url, headers=headers, timeout=self.timeout)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"GitHub API error: {response.status_code}")
                return None
        except Exception as e:
            print(f"GitHub API request failed: {e}")
            return None

    def get_repo_info(self, owner: str, repo: str) -> Optional[Dict[str, Any]]:
        """Get repository information with caching"""
        cache_key = self._get_cache_key(f"repos/{owner}/{repo}")

        # Check cache first
        if cache_key in self.cache:
            cache_data = self.cache[cache_key]
            if self._is_cache_valid(cache_data):
                return cache_data['data']

        # Make fresh request
        data = self._make_request(f"repos/{owner}/{repo}")
        if data:
            self.cache[cache_key] = {
                'data': data,
                'timestamp': time.time()
            }

        return data

    def get_latest_release(self, owner: str, repo: str) -> Optional[Dict[str, Any]]:
        """Get latest release information with caching"""
        cache_key = self._get_cache_key(f"repos/{owner}/{repo}/releases/latest")

        # Check cache first
        if cache_key in self.cache:
            cache_data = self.cache[cache_key]
            if self._is_cache_valid(cache_data):
                return cache_data['data']

        # Make fresh request
        data = self._make_request(f"repos/{owner}/{repo}/releases/latest")
        if data:
            self.cache[cache_key] = {
                'data': data,
                'timestamp': time.time()
            }

        return data
