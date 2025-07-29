# -*- coding: utf-8 -*-
"""
Testing module for user-agents handling
"""
from network.user_agents import UserAgent, ListUserAgent
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch
import httpx

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

@pytest_asyncio.fixture
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
    
class TestAsyncGetUpdatedUrlUserAgents:
    """Test class for ListUserAgent class
        scored_user_agent"""

    @pytest.mark.asyncio
    async def test_get_updated_url(self, list_user_agent):
        """Test if useragents.io URL is correctly connected"""
        url = await list_user_agent.get_updated_url_user_agents()
        assert "https://useragents.io/sitemaps/created/" in url

    @patch("httpx.AsyncClient.get")
    @pytest.mark.asyncio
    async def test_get_last_loc_tag(self, mock_get, list_user_agent):
        """Test if last loc is correctly fetched to update user agents list"""
        xml = """
        <sitemapindex>
            <sitemap><loc>https://useragents.io/sitemaps/created/2025/44/useragents.xml</sitemap>
            <sitemap><loc>https://useragents.io/sitemaps/created/2025/45/useragents.xml</loc></sitemap>
            <sitemap><loc>https://useragents.io/sitemaps/created/2025/46/useragents.xml</loc></sitemap>
        </sitemapindex>
        """
        mock_get.return_value.text = xml
        result = await list_user_agent.get_updated_url_user_agents()
        assert result == "https://useragents.io/sitemaps/created/2025/46/useragents.xml"

    @patch("httpx.AsyncClient.get")
    @patch("network.user_agents.ListUserAgent.get_cache_url_user_agents", return_value="cached_url")
    @pytest.mark.asyncio
    async def test_attribute_error_fallback(self, mock_cache, mock_get, list_user_agent):
        """Test if loc tag attribute error fallback works"""
        xml = """
            <sitemapindex>
                <sitemap><lastmod>2024-12-01</lastmod></sitemap>
            </sitemapindex>
        """
        mock_get.return_value.text = xml
        result = await list_user_agent.get_updated_url_user_agents()
        assert result == "cached_url"
        mock_cache.assert_awaited_once()

    @patch("httpx.AsyncClient.get", side_effect=httpx.ConnectTimeout("Timeout"))
    @patch("network.user_agents.ListUserAgent.get_cache_url_user_agents", return_value="cached_url")
    @pytest.mark.asyncio
    async def test_http_error_fallback(self, mock_cache, mock_get, list_user_agent):
        """Test if http error fallcback works"""
        result = await list_user_agent.get_updated_url_user_agents()
        assert result == "cached_url"
        mock_cache.assert_awaited_once()

    @patch("httpx.AsyncClient.get")
    @patch("network.user_agents.ListUserAgent.get_cache_url_user_agents", return_value="cached_url")
    @pytest.mark.asyncio
    async def test_index_error_fallback(self, mock_cache, mock_get, list_user_agent):
        """Test if xml index_error fallback works"""
        mock_get.return_value.text = "<sitemapindex></sitemapindex>"
        result = await list_user_agent.get_updated_url_user_agents()
        assert result == "cached_url"
        mock_cache.assert_awaited_once()

class TestListUserAgentFunctionnal():
    """Test class for ListUserAgent class functionnalities"""

    @pytest.mark.asyncio
    @patch.object(ListUserAgent, "save_cache_user_agents", new_callable=AsyncMock)
    @patch("network.user_agents.ListUserAgent.get_updated_url_user_agents", return_value="cached_url")
    @patch("network.user_agents.ListUserAgent.get_cache_url_user_agents", return_value="cached_url2")
    @patch.object(ListUserAgent, "get_updated_user_agents_list", new_callable=AsyncMock, return_value=[
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edge/134.0.0.0",
        ])
    async def test_get_data_from_site_unabled(self, mock_get_updated, mock_get_cache, mock_updated, mock_save, list_user_agent):
        """Test if user agents list is correctly updated from the site when enabling update is true and cache url is different than updated url from the site"""
        list_user_agent.enabling_update = True
        liste_user_agents = await list_user_agent.refresh_user_agents_list()
        # Verified that the methods were called in the correct order
        mock_get_updated.assert_awaited_once()
        mock_updated.assert_awaited_once()

        mock_save.assert_awaited_once_with([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edge/134.0.0.0",
        ])
        assert len(liste_user_agents) == 2
        assert await list_user_agent.compare_url_actualise_url_cache() is False
        assert all(isinstance(x, UserAgent) for x in liste_user_agents)
        
    @pytest.mark.asyncio
    @patch.object(ListUserAgent, "read_cache_user_agents", new_callable=AsyncMock, return_value={"absolute_url_not_found": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
            ]})
    @patch("network.user_agents.ListUserAgent.get_cache_url_user_agents", return_value="cached_url1")
    @patch("network.user_agents.ListUserAgent.get_updated_url_user_agents", return_value="cached_url1")
    @patch("httpx.AsyncClient.get", side_effect=httpx.HTTPError("Unauthorized"))
    async def test_get_data_on_site_timeout(self, mock_http, mock_get_updated_url, mock_get_cache, mock_read, list_user_agent):
        """Test if user agents list is correctly loaded from cache when the site is not reachable"""
        liste_user_agents = await list_user_agent.refresh_user_agents_list()
        mock_get_updated_url.assert_awaited_once()
        mock_get_cache.assert_awaited_once()
        mock_read.assert_awaited_once()
        assert len(liste_user_agents) == 2
        assert all(isinstance(x, UserAgent) for x in liste_user_agents)
        
    @pytest.mark.asyncio
    @patch("network.user_agents.os.path.exists", return_value=False)
    @patch("network.user_agents.ListUserAgent.get_cache_url_user_agents", return_value="absolute_url_not_found")
    @patch("network.user_agents.ListUserAgent.get_updated_url_user_agents", return_value="absolute_url_not_found")
    @patch("httpx.AsyncClient.get", side_effect=httpx.HTTPError("Unauthorized"))
    async def test_get_data_on_site_and_cache_disabled(self, mock_http, mock_updated_url, mock_cache_url, mock_read_cache, list_user_agent):
        """Test if user agents list is correctly loaded from the backup in-code when site and cache are disabled"""
        safe_callback = {
            "absolute_url_not_found": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
            ]
        }
        liste_user_agents = await list_user_agent.refresh_user_agents_list()
        mock_updated_url.assert_awaited_once()
        fallback_dict = await list_user_agent.read_cache_user_agents()
        assert fallback_dict == safe_callback
        assert len(liste_user_agents) == 2
        assert all(isinstance(x, UserAgent) for x in liste_user_agents)

