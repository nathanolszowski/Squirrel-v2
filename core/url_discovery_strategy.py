# -*- coding: utf-8 -*-
"""
Url Discovery Strategy module.
This module defines the UrlDiscoveryStrategy class, which is responsible for discovering URLs based on a given strategy.
"""

from abc import ABC, abstractmethod
import logging
from selectolax.parser import HTMLParser
from network.http_client_handler import AsyncClientHandler

logger = logging.getLogger(__name__)

class UrlStrategy(ABC):
    @abstractmethod
    async def discover_urls(self, start_link:str, http_client:AsyncClientHandler) -> list[str]:
        pass
    
class SitemapStrategy(UrlStrategy):
    async def discover_urls(self, start_link:str, http_client:AsyncClientHandler) -> list[str]:
        logger.info("Fetch urls from xml sitemap")
        failed_urls = []
        try:
            urls = []
            if isinstance(start_link, dict):
                logger.info("Fetching urls from multiple sitemaps")
                for actif, url in start_link.items():
                    async with http_client as client:
                        response = await client.get(url)
                    if response is None:
                        logger.warning(f"No response from : {url}")
                        return []
                    page = HTMLParser(response.text)
                    for node in page.css("url"):
                        loc_node = node.css_first("loc")
                        if loc_node:
                            urls.append(loc_node.text())
            else:
                logger.info("Fetching urls from a single sitemap")
                async with http_client as client:
                    response = await client.get(start_link)
                    if response is None:
                        logger.warning(f"No response from : {start_link}")
                        return []
                page = HTMLParser(response.text)
                for node in page.css("url"):
                    loc_node = node.css_first("loc")
                    if loc_node:
                        urls.append(loc_node.text())
            return urls

        except Exception as e:
            logger.error(
                f"Error when fetching urls from {start_link}: {e}"
            )
            return []
    
class PaginationStrategy(UrlStrategy):
    async def discover_urls(self, start_link:str, http_client:AsyncClientHandler) -> list[str]:
        pass
    
class APIStrategy(UrlStrategy):
    async def discover_urls(self, start_link:str, http_client:AsyncClientHandler) -> list[str]:
        pass
    
def URLDiscoveryStrategy(url_strategy:str) -> UrlStrategy:
    strategies = {
        "XML": SitemapStrategy,
        "URL": PaginationStrategy,
        "API": APIStrategy
    }
    try:
        return strategies[url_strategy]()
    except KeyError:
        raise ValueError(f"Stratégie inconnue : {url_strategy}")