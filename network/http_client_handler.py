# -*- coding: utf-8 -*-
"""
Class to handle HTTP requests.
This module provides a class `ClientHandler` that manages HTTP requests.
It includes methods for making GET and POST requests with optional headers, user-agent and proxy.
"""

import httpx


class ClientHandler:
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
        self.client = httpx.Client(proxies=self.proxy) if self.proxy else httpx.Client()

    def get_user_agent(self):
        pass

    def get(self, url, headers=None):
        """
        Effectue une requête GET sur l'URL spécifiée.

        Args:
            url (str): L'URL à laquelle faire la requête.
            headers (dict, optional): En-têtes HTTP à inclure dans la requête.

        Returns:
            Response: La réponse de la requête HTTP.
        """
        return self.client.get(url, headers=headers)
