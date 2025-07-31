# -*- coding: utf-8 -*-
"""
Testing module for http client handling
Unitest tests:
_rotate_session() >	ancien client fermé, nouveau client actif
_request()	> retry + délai entre appels
get_user_agent() >	UA chargé et stocké
get_proxy()	> retourne None ou une IP (mockée)

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
from unittest.mock import AsyncMock, patch


class TestUnitAsyncClientHandler:
    """Test class for unitesting AsyncClientHandler class"""
    
    @pytest.mark.asyncio
    @patch("network.http_client_handler.AsyncClientHandler.get_user_agent", return_value="TestUA/1.0")
    async def test_setup_client_sets_headers():
        handler = AsyncClientHandler(proxy=None)

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value = mock_instance

            await handler.setup_client()

            assert handler.client is not None
            assert "User-Agent" in handler.client.headers
            assert handler.client.headers["User-Agent"] == "TestUA/1.0"
            
    @pytest.mark.asyncio
    @patch("network.http_client_handler.AsyncClientHandler.get_user_agent", return_value="TestUA/1.0")
    async def test_setup_client_sets_proxy():
        handler = AsyncClientHandler(proxy="http://testproxy:8080")
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value = mock_instance

            await handler.setup_client()
            
            assert handler.client is not None
            assert handler.proxy == "http://testproxy:8080"


"""
@pytest_asyncio.fixture
async def list_user_agent():
    client = AsyncClientHandler(proxy=None)
    await client.setup_client()
    return client
"""