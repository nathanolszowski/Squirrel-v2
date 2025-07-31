# -*- coding: utf-8 -*-
"""
Testing module for http client handling
Unitest tests:
_rotate_session() >	ancien client fermé, nouveau client actif
_request()	> retry + délai entre appels

Func tests :
Requête GET sur un site test (httpbin) >	Connexion, UA correct, status 200
Requête via proxy	> Le proxy est bien utilisé
Rotation de session effective >	Changement d’UA au-delà du reset_threshold
Cookies persistés entre requêtes >	handler.client.cookies contient les bons cookies
Liste d’URLs KO enregistrée >	failed_urls contient bien les échecs
"""

import pytest
import pytest_asyncio
from network.http_client_handler import AsyncClientHandler
from unittest.mock import AsyncMock, patch, MagicMock
from httpx import Response


class TestUnitAsyncClientHandler:
    """Test class for unitesting AsyncClientHandler class"""
    
    @pytest.mark.asyncio
    @patch("network.http_client_handler.AsyncClientHandler.get_user_agent", return_value="TestUA/1.0")
    async def test_setup_client_with_headers(self, mock_get_user_agent):
        handler = AsyncClientHandler(proxy=None)

        with patch("httpx.AsyncClient") as mock_client:
            await handler.setup_client()

            mock_client.assert_called_once()
            kwargs = mock_client.call_args.kwargs
            assert handler.client is not None
            assert kwargs["headers"]["User-Agent"] == "TestUA/1.0"

    @pytest.mark.asyncio
    @patch("network.http_client_handler.AsyncClientHandler.get_user_agent", return_value="TestUA/1.0")
    @patch("httpx.AsyncClient.get")
    @pytest.mark.parametrize(
        "proxy, mock_status, expected_proxy_ok",
        [
            ("http://testproxy:8080", 200, True),
            ("http://testproxy:8080", 403, False),
            (None, 200, False),
        ],
    )
    async def test_client_set_proxy(
        self,
        mock_httpx_get,
        mock_get_user_agent,
        proxy,
        mock_status,
        expected_proxy_ok,
    ):
        # Mock la réponse du GET vers httpbin
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = mock_status
        mock_response.raise_for_status.side_effect = (
            None if mock_status == 200 else Exception("Forbidden")
        )
        mock_response.json.return_value = {"origin": "1.2.3.4"}
        mock_httpx_get.return_value = mock_response

        handler = AsyncClientHandler(proxy=proxy)

        with patch("httpx.AsyncClient.__aenter__", return_value=AsyncMock(get=mock_httpx_get)):
            with patch("httpx.AsyncClient.__aexit__", return_value=None):
                await handler.setup_client()

        assert handler.client is not None
        assert handler.proxy == proxy
        assert handler.proxy_ok == expected_proxy_ok

    @pytest.mark.asyncio
    @patch("network.http_client_handler.AsyncClientHandler.get_user_agent", return_value="NewTestUA/1.0")
    @patch("network.http_client_handler.AsyncClientHandler.setup_client")
    async def test_client_rotate_session(self, mock_setup_client, mock_get_user_agent):
        handler = AsyncClientHandler(proxy=None)
        # client initial (doit être fermé)
        old_client = AsyncMock()
        handler.client = old_client
        # simulate UA + state
        handler.user_agent = "OldUA"
        handler.request_count = 30
        handler.reset_threshold = 40
        await handler._rotate_session()
        # le client initial doit être fermé
        old_client.aclose.assert_awaited_once()
        # new client setup
        mock_setup_client.assert_awaited_once()
        # check new states
        assert handler.request_count == 0
        assert 20 <= handler.reset_threshold <= 40
        assert handler.user_agent == "NewTestUA/1.0"


"""
@pytest_asyncio.fixture
async def list_user_agent():
    client = AsyncClientHandler(proxy=None)
    await client.setup_client()
    return client
"""