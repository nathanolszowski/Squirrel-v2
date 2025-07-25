# -*- coding: utf-8 -*-
"""
Class to handle HTTP requests.
This module provides a class `ClientHandler` that manages HTTP requests.
It includes methods for making GET and POST requests with optional headers, user-agent and proxy.
"""

# utils/http_client.py

import random
import asyncio
import httpx
from typing import Optional


class HttpClient:
    def __init__(
        self,
        max_retries: int = 3,
        timeout: float = 10.0,
        backoff_factor: float = 0.5,
        user_agent: Optional[str] = None,
    ):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.timeout = timeout

        self._client = httpx.AsyncClient(
            headers=self._build_headers(user_agent), timeout=httpx.Timeout(timeout)
        )

    def _build_headers(self, user_agent: Optional[str]) -> dict:
        return {
            "User-Agent": user_agent or get_random_user_agent(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "fr-FR,fr;q=0.9",
        }

    async def get(self, url: str, **kwargs) -> httpx.Response:
        return await self._request_with_retry("GET", url, **kwargs)

    async def post(self, url: str, data=None, **kwargs) -> httpx.Response:
        return await self._request_with_retry("POST", url, data=data, **kwargs)

    async def _request_with_retry(
        self, method: str, url: str, **kwargs
    ) -> httpx.Response:
        for attempt in range(1, self.max_retries + 1):
            try:
                response = await self._client.request(method, url, **kwargs)
                response.raise_for_status()
                return response
            except (httpx.RequestError, httpx.HTTPStatusError) as exc:
                if attempt == self.max_retries:
                    raise
                wait_time = self.backoff_factor * attempt
                print(
                    f"[Retry {attempt}] Erreur sur {url}: {exc}. Attente de {wait_time:.1f}s."
                )
                await asyncio.sleep(wait_time)

    async def close(self):
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
