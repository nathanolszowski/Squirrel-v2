# -*- coding: utf-8 -*-
"""
Class to handle HTTP requests.
This module provides a class `ClientHandler` that manages HTTP requests.
It includes methods for making GET and POST requests with optional headers, user-agent and proxy.
"""

import httpx


class AsyncClientHandler:
    """
    Class to handle HTTP requests.
    """

    def __init__(self, proxy):
        """
        Initializes the ClientHandler with a specific HTTP client.

        Args:
            http_client: An instance of an HTTP client that implements methods like `get` and `post`.
        """
        self.proxy = proxy
        self._client = httpx.AsyncClient()

    async def get_user_agent(self):
        pass

    async def get(self, url, headers=None):
        """
        Sends a GET request to the specified URL.

        Args:
            url (str): URL to send the GET request to.
            headers (dict, optional): HTTP headers.

        Returns:
            Response: Response from the GET request.
        """
        return await self._client.get(url, headers=None)

    async def post(self, url, data=None, headers=None):
        """
        Sends a POST request to the specified URL.

        Args:
            url (str): URL to send the POST request to.
            headers (dict, optional): HTTP headers.

        Returns:
            Response: Response from the POST request.
        """
        return await self._client.post(url, data=data, headers=headers)

    async def close(self):
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
