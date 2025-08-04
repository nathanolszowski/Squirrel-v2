# -*- coding: utf-8 -*-
"""
Url Discovery Strategy module.
This module defines the UrlDiscoveryStrategy class, which is responsible for discovering URLs based on a given strategy.
"""

from abc import ABC, abstractmethod

class UrlStrategy(ABC):
    @abstractmethod
    async def discover_urls(self, url: str) -> list[str]:
        pass
    
class SitemapStrategy(UrlStrategy):
    async def discover_urls(self, url: str) -> list[str]:
        pass
    
class PaginationStrategy(UrlStrategy):
    async def discover_urls(self, url: str) -> list[str]:
        pass
    
def URLDiscoveryStrategy(url_strategy: str) -> UrlStrategy:
    if url_strategy == "XML":
        return SitemapStrategy()
    elif url_strategy == "URL":
        return PaginationStrategy()
    raise ValueError(f"Stratégie inconnue : {url_strategy}")