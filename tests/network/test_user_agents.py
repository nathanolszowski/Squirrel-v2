# -*- coding: utf-8 -*-
"""
Testing module for user-agents handling
"""
from network.user_agents import UserAgent, ListUserAgent
import pytest


class TestUserAgent:
    """Test class for UserAgent class"""

    @pytest.mark.parametrize(
        "ua_string, expected_browser, expected_os",
        [
            (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                "Chrome",
                "Windows",
            ),
            (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
                "Safari",
                "Mac OS X",
            ),
            (
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0",
                "Firefox",
                "Ubuntu",
            ),
            (
                "Mozilla/5.0 (Linux; Android 11; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
                "Chrome Mobile",
                "Android",
            ),
        ],
    )
    def test_initialisation(self, ua_string, expected_browser, expected_os):
        ua = UserAgent(ua_string)
        assert ua.browser == expected_browser
        assert ua.os == expected_os
        assert isinstance(ua.browser_version, int)

class TestAsyncListUserAgent:
    """Test class for ListUserAgent class
        scored_user_agent"""
        
    @pytest.fixture
    async def list_user_agent():
        ua_strings = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0",
        "Mozilla/5.0 (Linux; Android 11; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36"
        ]
        ua = ListUserAgent()
        await ua.load_user_agents_list(ua_strings)
        return ua
    
    def test_get_updated_url(self):
        pass