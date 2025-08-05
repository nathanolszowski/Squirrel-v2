# -*- coding: utf-8 -*-
"""
Class to handle HTTP requests.
This module provides a class `ClientHandler` that manages HTTP requests.
It includes methods for making GET and POST requests with optional headers, user-agent and proxy.
"""

import httpx
from network.user_agents import ListUserAgent
import logging
import random
import asyncio
from config.squirrel_settings import REQUEST_TIMEOUT, PROXY

logger = logging.getLogger(__name__)

class AsyncClientHandler:
    """
    Class to handle HTTP requests.
    """

    def __init__(self):
        """
        Initializes the ClientHandler with a specific HTTP client.

        Args:
            http_client: An instance of an HTTP client that implements methods like `get` and `post`.
        """
        self.proxy: str | None = PROXY if PROXY else None
        self.proxy_ok: bool = False
        self.user_agent_liste: ListUserAgent | None = None
        self.failed_urls: list[str] = []
        self.request_count: int = 0
        self.retry_attempts: int = 3
        self.reset_threshold: int = random.randint(20, 40)  # Changement de session
        
    async def setup_client(self) -> httpx.AsyncClient:
        """Sets up the HTTP client with settings."""
        self.user_agent = await self._get_user_agent()
        proxy = await self._get_proxy()
        self.client = httpx.AsyncClient(proxy=proxy,
                        headers={"User-Agent": self.user_agent},
                        timeout=REQUEST_TIMEOUT,
                        follow_redirects=True,
                    )
        return self.client
    
    async def _request(
        self,
        method: str,
        url: str,
        headers: dict | None = None,
        data=None,
        max_retries: int = 3,
        backoff_factor: float = 0.5
    ) -> httpx.Response | None:
        if not self.client:
            await self.setup_client()

        final_headers = self.client.headers.copy()
        if headers:
            final_headers.update(headers)

        for attempt in range(1, max_retries + 1):
            try:
                response = await self.client.request(method, url, headers=final_headers, data=data)
                response.raise_for_status()
                self.request_count += 1
                if self.request_count >= self.reset_threshold:
                    await self._rotate_session()
                await asyncio.sleep(random.uniform(0.8, 2.5))
                return response
            except (httpx.RequestError, httpx.HTTPStatusError) as e:
                if attempt == max_retries:
                    return None
                await asyncio.sleep(backoff_factor * (2 ** (attempt - 1)))

    async def _rotate_session(self):
        """Rotate the HTTP session after a certain number of requests."""
        logger.info("Rotate http session after %d request", self.request_count)
        if self.client:
            await self.client.aclose()
        self.request_count = 0
        self.reset_threshold = random.randint(20, 40)
        self.user_agent = await self._get_user_agent()
        self.client = await self.setup_client()

    async def get(self, url: str, headers: dict | None = None) -> httpx.Response | None:
        return await self._request("GET", url, headers=headers)

    async def post(self, url: str, data=None, headers: dict | None = None) -> httpx.Response | None:
        return await self._request("POST", url, headers=headers, data=data)
    
    async def __aenter__(self):
        """Initialize the http client when entering the context."""
        if not self.client:
            await self.setup_client()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close the http client when exiting the context."""
        await self.client.aclose()

    async def _init_user_agents_list(self) -> ListUserAgent:
        """Returns a user-agents list for header usage.
        
        Returns:
            self.user_agent_liste (ListUserAgent) : a list of user-agents.
        """
        self.user_agent_liste = ListUserAgent()
        await self.user_agent_liste.refresh_user_agents_list()
        return self.user_agent_liste         

    async def _get_user_agent(self) -> str:
        """Returns a user-agent string for header usage.
        
        Returns:
            self.user_agent (str) : a scored user-agents.
        """
        if self.user_agent_liste is None:
            self.user_agent_liste = await self._init_user_agents_list()
        self.user_agent = self.user_agent_liste.get_user_agent()
        return self.user_agent
    
    async def _get_proxy(self) -> str | None:
        """Returns the proxy used by the client.
        
        Returns:
            self.proxy (str | None) : the proxy used by the client.
            None if no proxy is available or if the proxy is invalid.
        """
        if self.proxy is None:
            logger.info("No proxy available.")
            return None

        try:
            async with httpx.AsyncClient(proxy=self.proxy, timeout=5.0) as client:
                response = await client.get("https://httpbin.org/ip")
                response.raise_for_status()
                ip = response.json().get("origin")
                logger.info(f"Proxy avilable, IP : {ip}")
                self.proxy_ok = True
                return self.proxy
        except Exception as e:
            logger.warning(f"Proxy unvailable or invalid : {e}")
            self.proxy_ok = False
            return None