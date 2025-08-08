# -*- coding: utf-8 -*-
"""
Testing module for http client handling
"""

import pytest
from network.client_handler import HTTPClientHandler, HeadlessClientHandler
from unittest.mock import AsyncMock, patch, MagicMock
from httpx import Response
import httpx
import warnings

warnings.filterwarnings("ignore", category=pytest.PytestUnraisableExceptionWarning)
warnings.filterwarnings("ignore", category=ResourceWarning)

class TestHTTPClientHandler:
    """Test class for unitesting HTTPClientHandler class"""
    
    @pytest.mark.asyncio
    @patch("network.client_handler.HTTPClientHandler._get_user_agent", return_value="TestUA/1.0")
    async def test_setup_client_with_headers(self, mock_get_user_agent):
        handler = HTTPClientHandler()

        with patch("httpx.AsyncClient") as mock_client:
            await handler.setup_client()

            mock_client.assert_called_once()
            kwargs = mock_client.call_args.kwargs
            assert handler.client is not None
            assert kwargs["headers"]["User-Agent"] == "TestUA/1.0"
    
    @pytest.mark.asyncio
    @patch("network.client_handler.HTTPClientHandler._get_user_agent", return_value="TestUA/1.0")
    @patch("httpx.AsyncClient.get")
    async def test_get_proxy_success(
        self,
        mock_httpx_get,
        mock_get_user_agent
    ):
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"origin": "1.2.3.4"}
        mock_httpx_get.return_value = mock_response
        with patch("network.client_handler.PROXY", "http://testproxy:8080"):
            handler = HTTPClientHandler()
        with patch("httpx.AsyncClient.__aenter__", return_value=AsyncMock(get=mock_httpx_get)):
            with patch("httpx.AsyncClient.__aexit__", return_value=None):
                proxy_used = await handler._get_proxy()

        assert proxy_used == "http://testproxy:8080"
        assert handler.proxy_ok is True
        
    @pytest.mark.asyncio
    @patch("network.client_handler.HTTPClientHandler._get_user_agent", return_value="TestUA/1.0")
    @patch("httpx.AsyncClient.get")
    async def test_get_proxy_failure(
        self,
        mock_httpx_get,
        mock_get_user_agent
    ):
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.raise_for_status.side_effect = Exception("Forbidden")
        mock_response.json.return_value = {"origin": "1.2.3.4"}
        mock_httpx_get.return_value = mock_response
        
        with patch("network.client_handler.PROXY", "http://testproxy:8080"):
            handler = HTTPClientHandler()
        with patch("httpx.AsyncClient.__aenter__", return_value=AsyncMock(get=mock_httpx_get)):
            with patch("httpx.AsyncClient.__aexit__", return_value=None):
                proxy_used = await handler._get_proxy()

        assert proxy_used == None
        assert handler.proxy_ok is False
        
    @pytest.mark.asyncio
    @patch("network.client_handler.HTTPClientHandler._get_user_agent", return_value="NewTestUA/1.0")
    @patch("network.client_handler.HTTPClientHandler.setup_client")
    async def test_client_rotate_session(self, mock_setup_client, mock_get_user_agent):
        """Test the session rotation after a certain number of requests."""
        
        handler = HTTPClientHandler()
        old_client = AsyncMock()
        handler.client = old_client
        handler.user_agent = "OldUA"
        handler.request_count = 30
        handler.reset_threshold = 40
        await handler._rotate_session()
        old_client.aclose.assert_awaited_once()
        
        # new client setup
        mock_setup_client.assert_awaited_once()
        
        # check new states
        assert handler.request_count == 0
        assert 20 <= handler.reset_threshold <= 40
        assert handler.user_agent == "NewTestUA/1.0"

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "side_effects, expected_status, expected_in_failed, url",
        [
            (
                [
                    httpx.RequestError("fail 1", request=httpx.Request("GET", "https://example.com")),
                    httpx.RequestError("fail 2", request=httpx.Request("GET", "https://example.com")),
                    httpx.Response(200, request=httpx.Request("GET", "https://example.com")),
                ],
                200,
                False,
                "https://example.com"
            ),
            (
                [
                    httpx.RequestError("fail 1", request=httpx.Request("GET", "https://fail.me")),
                    httpx.RequestError("fail 2", request=httpx.Request("GET", "https://fail.me")),
                    httpx.RequestError("fail 3", request=httpx.Request("GET", "https://fail.me")),
                ],
                None,
                True,
                "https://fail.me"
            )
        ]
    )
    @patch("network.client_handler.HTTPClientHandler._get_user_agent", return_value="TestUA/1.0")
    @patch("network.client_handler.HTTPClientHandler.setup_client")
    async def test_request_parametrized(
        self,
        mock_setup_client,
        mock_get_user_agent,
        side_effects,
        expected_status,
        expected_in_failed,
        url
    ):
        """Test the _request method with success and fail."""
        
        handler = HTTPClientHandler()
        handler.client = AsyncMock()
        handler.client.request.side_effect = side_effects

        response = await handler._request(
            method="GET",
            url=url,
            max_retries=3,
            backoff_factor=0
        )

        if expected_status:
            assert isinstance(response, httpx.Response)
            assert response.status_code == expected_status
        else:
            assert response is None
            
class TestHeadlessClientHandler:
    """Test class for unitesting HeadlessClient class"""
    
    @pytest.mark.asyncio
    @patch('network.client_handler.async_playwright')
    @patch('network.client_handler.AsyncCamoufox')
    async def test_setup_client_camoufox_success(self, mock_camoufox_class, mock_playwright_class):
        """Test Camoufox OK."""
        handler = HeadlessClientHandler()
        handler._get_user_agent = AsyncMock(return_value='agent-test')
        handler._get_proxy = AsyncMock(return_value='proxy-test')
        handler.camoufox = True

        mock_browser = AsyncMock(name="MockCamoufoxBrowser")
        mock_browser.close = AsyncMock()
        mock_camoufox = AsyncMock()
        mock_camoufox.__aenter__.return_value = mock_browser
        mock_camoufox_class.return_value = mock_camoufox

        await handler.setup_client()
        assert handler.browser == mock_browser
        assert handler.context is None
        
        await handler._close_client()
        mock_camoufox.__aexit__.assert_awaited()

    @pytest.mark.asyncio
    @patch('network.client_handler.async_playwright')
    @patch('network.client_handler.AsyncCamoufox', side_effect=Exception("Erreur Camoufox"))
    async def test_setup_client_camoufox_fail_fallback_chromium(self, mock_camoufox_class, mock_playwright_class):
        """Test fallback Chromium si Camoufox KO."""
        handler = HeadlessClientHandler()
        handler._get_user_agent = AsyncMock(return_value='agent-test')
        handler._get_proxy = AsyncMock(return_value='proxy-test')
        handler.camoufox = True

        # Mock Playwright + browser/context
        mock_playwright = AsyncMock()
        mock_browser = AsyncMock(name="MockBrowserChromium")
        mock_context = AsyncMock(name="MockContextChromium")
        mock_context.close = AsyncMock()
        mock_browser.close = AsyncMock()
        mock_playwright.stop = AsyncMock()
        mock_playwright.start.return_value = mock_playwright
        mock_playwright.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_playwright_class.return_value = mock_playwright

        await handler.setup_client()
        assert handler.browser == mock_browser
        assert handler.context == mock_context
        
        await handler._close_client()
        mock_context.close.assert_awaited()
        mock_browser.close.assert_awaited()
        mock_playwright.stop.assert_awaited()

    @pytest.mark.asyncio
    @patch('network.client_handler.async_playwright')
    async def test_setup_client_chromium_default(self, mock_playwright_class):
        """Test Chromium lancé directement (camoufox désactivé)."""
        handler = HeadlessClientHandler()
        handler._get_user_agent = AsyncMock(return_value='default-agent')
        handler._get_proxy = AsyncMock(return_value=None)
        handler.camoufox = False

        # Mock Playwright + browser/context
        mock_playwright = AsyncMock()
        mock_browser = AsyncMock(name="MockBrowserChromium")
        mock_context = AsyncMock(name="MockContextChromium")
        mock_context.close = AsyncMock()
        mock_browser.close = AsyncMock()
        mock_playwright.stop = AsyncMock()
        mock_playwright.start.return_value = mock_playwright
        mock_playwright.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_playwright_class.return_value = mock_playwright

        await handler.setup_client()
        assert handler.browser == mock_browser
        assert handler.context == mock_context
        
        await handler._close_client()
        mock_context.close.assert_awaited()
        mock_browser.close.assert_awaited()
        mock_playwright.stop.assert_awaited()
    """
    @pytest.mark.asyncio
    async def test_goto_real_url_chromium(self):
        url = "https://example.com"

        async with HeadlessClientHandler(headless=True) as handler:
            handler.camoufox = False
            handler._get_user_agent = AsyncMock(return_value="MonUserAgentTest/1.0")
            await handler.setup_client()
            html = await handler.goto(url, wait_until="domcontentloaded")
            
        assert "<html" in html.lower()
        assert "example" in html.lower()
    """
