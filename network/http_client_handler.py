# -*- coding: utf-8 -*-
"""
Class to handle HTTP requests.
This module provides a class `ClientHandler` that manages HTTP requests.
It includes methods for making GET and POST requests with optional headers, user-agent and proxy.
"""

import httpx
from network.user_agents import ListUserAgent
import logging
from config.squirrel_settings import REQUEST_TIMEOUT

logger = logging.getLogger(__name__)

class AsyncClientHandler:
    """
    Class to handle HTTP requests.
    """

    def __init__(self, proxy: str):
        """
        Initializes the ClientHandler with a specific HTTP client.

        Args:
            http_client: An instance of an HTTP client that implements methods like `get` and `post`.
        """
        self.proxy = proxy
        self.user_agent_liste: ListUserAgent | None = None
        self.failed_urls: list[str] = []
        self.retry_attempts: int = 3
        
    async def setup_client(self) -> httpx.AsyncClient:
        """Sets up the HTTP client with settings."""
        self.user_agent = await self.get_user_agent()
        self.client = httpx.AsyncClient(proxy=self.proxy,
                        headers={"User-Agent": self.user_agent},
                        timeout=REQUEST_TIMEOUT,
                        follow_redirects=True,
                    )
        return self.client

    async def client_get_method(self, url: str, headers: dict | None) -> httpx.Response:
        """
        Sends a GET request to the specified URL.

        Args:
            url (str): URL to send the GET request to.
            headers (dict, optional): HTTP headers.

        Returns:
            Response: Response from the GET request.
        """
        if not self.client:
            await self.setup_client()

        final_headers = self.client.headers.copy()
        if headers:
            final_headers.update(headers)

        response = await self.client.get(url, headers=final_headers)
        response.raise_for_status()
        return response

    async def client_post_method(self, url: str, data: dict | None, headers: dict | None) -> httpx.Response:
        """
        Sends a POST request to the specified URL.

        Args:
            url (str): URL to send the POST request to.
            headers (dict, optional): HTTP headers.

        Returns:
            Response: Response from the POST request.
        """
        if not self.client:
            await self.setup_client()

        final_headers = self.client.headers.copy()
        if headers:
            final_headers.update(headers)

        response = await self.client.post(url, data=data, headers=final_headers)
        response.raise_for_status()
        return response

    async def client_retry_request(self):
        """Method to retry a request if it fails."""
        pass
    
    async def close_client(self) -> None:
        """Close the client properly"""
        if self.client:
            await self.client.aclose()

    async def init_user_agents_list(self) -> ListUserAgent:
        """Returns a user-agents list for header usage.
        
        Returns:
            self.user_agent_liste : a list of user-agents.
        """
        self.user_agent_liste = ListUserAgent()
        await self.user_agent_liste.refresh_user_agents_list()
        return self.user_agent_liste         

    async def get_user_agent(self):
        """Returns a user-agent string for header usage.
        
        Returns:
            self.user_agent : a scored user-agents.
        """
        if self.user_agent_liste is None:
            self.user_agent_liste = await self.init_user_agents_list()
        user_agent = self.user_agent_liste.get_user_agent()
        return user_agent
