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
from typing import Any
from playwright.async_api import async_playwright
from camoufox.async_api import AsyncCamoufox
from config.squirrel_settings import HTTP_TIMEOUT, PROXY, CAMOUFOX

logger = logging.getLogger(__name__)

class AsyncClientHandler:
    """AsyncClientHandler is a base class for all clients.
    This class manages proxy and user agents.
    """
    
    def __init__(self):
        self.proxy: str | None = PROXY if PROXY else None
        self.proxy_ok: bool = False
        self.user_agent_liste: ListUserAgent | None = None
    
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
            async with httpx.AsyncClient(proxy=self.proxy, follow_redirects=True, timeout=5.0) as client:
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
        
    async def _init_user_agents_list(self) -> ListUserAgent:
        """Returns a user-agents list for header usage.
        
        Returns:
            self.user_agent_liste (ListUserAgent) : a list of user-agents.
        """
        self.user_agent_liste = ListUserAgent()
        await self.user_agent_liste.refresh_user_agents_list()
        return self.user_agent_liste         

    async def _get_user_agent(self) -> str:
        self.user_agent = self.user_agent_liste.get_user_agent()
        return self.user_agent

class HTTPClientHandler(AsyncClientHandler):
    """
    Class to handle HTTP requests.
    """

    def __init__(self) -> None:
        """Initializes the Client with a specific HTTP client."""
        super().__init__()
        self.failed_urls: list[str] = []
        self.request_count: int = 0
        self.retry_attempts: int = 3
        self.reset_threshold: int = random.randint(20, 40)  # Changement de session
        
    async def setup_client(self) -> httpx.AsyncClient:
        """Sets up the HTTP client with settings."""
        await self._init_user_agents_list()
        self.user_agent = await self._get_user_agent()
        self.proxy = await self._get_proxy()
        await self._init_httpx_client()
        return self.client
    
    async def _init_httpx_client(self):
        self.client = httpx.AsyncClient(
            proxy=self.proxy if self.proxy_ok else None,
            headers={"User-Agent": self.user_agent},
            timeout=HTTP_TIMEOUT,
            follow_redirects=True,
        )
    
    async def _request(
        self,
        method: str,
        url: str,
        headers: dict | None = None,
        data=None,
        max_retries: int = 3,
        backoff_factor: float = 0.5
    ) -> httpx.Response | None:
        """Manages all query logic for different types of queries

        Args:
            method (str): Represents the type of request
            url (str): Path to the resource
            headers (dict | None, optional): Contains all the requests parameters. Defaults to None.
            data (_type_, optional): Contains all the datas sent to the server to collect specific resource. Defaults to None.
            max_retries (int, optional): Represents the number of retries accepted for a request when it can't reach the resource the first time. Defaults to 3.
            backoff_factor (float, optional): Represents a float used as a factor to calculate a wait time after multiple requests to the same resource.. Defaults to 0.5.

        Returns:
            httpx.Response | None: Returns an http response or None if the request can't reach the resource
        """
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

    async def _rotate_session(self) -> None:
        """Rotate the HTTP session after a certain number of requests."""
        logger.info("Rotate http session after %d request", self.request_count)
        if self.client:
            await self.client.aclose()
        self.request_count = 0
        self.reset_threshold = random.randint(20, 40)
        await self.setup_client()

    async def get(self, url: str, headers: dict | None = None) -> httpx.Response | None:
        """GET method for the HTTP client, used to collect data from a specified resource

        Args:
            url (str): Path to the resource
            headers (dict | None, optional): Contains all the requests parameters. Defaults to None.

        Returns:
            httpx.Response | None: Returns an http response or None if the request can't reach the resource
        """
        return await self._request("GET", url, headers=headers)

    async def post(self, url: str, data:dict|None= None, headers: dict|None = None) -> httpx.Response | None:
        """GET method for the HTTP client, used to collect data from a specified resource

        Args:
            url (str): Path to the resource
            headers (dict|None, optional): Contains all the requests parameters. Defaults to None.
            data (dict|None): Contains all the datas sent to the server to collect specific resource. Defaults to None.

        Returns:
            httpx.Response | None: Returns an http response or None if the request can't reach the resource
        """
        return await self._request("POST", url, headers=headers, data=data)
    
    async def __aenter__(self):
        """Initialize the http client when entering the context."""
        if not hasattr(self, "client") or self.client is None:
            await self.setup_client()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Close the http client when exiting the context."""
        await self.client.aclose()
        
class HeadlessClientHandler(AsyncClientHandler):
    """
    Class to handle requests throught an headless browser like Playwright.
    """
    
    def __init__(self, headless:bool = True) -> None:
        """Initializes the Client with a specific headless browser."""
        super().__init__()
        self.browser:Any = None
        self.playwright:Any = None
        self.headless = headless
        self.context = None
        self.camoufox = CAMOUFOX
        self._camoufox_ctx:Any = None
               
    async def setup_client(self):
        """This method choose if the client used the default browser or a special scraping browser named Camoufox."""
        await self._init_user_agents_list()
        self.user_agent = await self._get_user_agent()
        proxy = await self._get_proxy()
        if self.camoufox:
            try:
                await self._launch_camoufox_browser(proxy)
            except Exception as e:
                logger.warning(f"Enabling to use Camoufox : {e} Use default browser.")
                await self._launch_default_browser(proxy)
        else:
            await self._launch_default_browser(proxy)
            
    async def _launch_camoufox_browser(self, proxy):
        """Start client with Camoufox browser."""
        logger.info("Starting client with Camoufox browser")
        self._camoufox_ctx = AsyncCamoufox(
            headless=self.headless,
            proxy={"server": proxy} if proxy else None,
        )
        self.browser = await self._camoufox_ctx.__aenter__()
        self.context = None

    async def _launch_default_browser(self, proxy) -> None:
        """Start client with default chromium browser."""
        logger.info("Starting client with default Chromium browser")
        self.playwright = await async_playwright().start()
        browser_args:dict|Any = {"headless": self.headless}
        if proxy:
            browser_args["proxy"] = {"server": proxy}
        self.browser = await self.playwright.chromium.launch(**browser_args)
        self.context = await self.browser.new_context(user_agent=self.user_agent)
            
    async def __aenter__(self):
        """Initialize the http client when entering the context."""
        if not hasattr(self, "client") or self.client is None:
            await self.setup_client()
        return self
    
    async def _close_client(self, exc_type=None, exc=None, tb=None) -> None:
        """Close the client properly no matter which default or camoufox browser is used"""
        if self.context is not None:
            await self.context.close()
            self.context = None

        if self.browser is not None:
            if self._camoufox_ctx is not None:
                try:
                    await self._camoufox_ctx.__aexit__(exc_type, exc, tb)
                finally:
                    self._camoufox_ctx = None
                    self.browser = None
            else:
                await self.browser.close()
                self.browser = None

        if self.playwright is not None:
            await self.playwright.stop()
            self.playwright = None
        await asyncio.sleep(0)
        logger.info("Browser and Playwright are closed.")

    async def __aexit__(self, exc_type, exc, tb) -> None:
        """Finally close the client"""
        await self._close_client(exc_type, exc, tb)