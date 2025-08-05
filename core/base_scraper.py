# -*- coding: utf-8 -*-
"""
Base Scraper module.
This module provides a base class for scrapers, defining the common interface and functionnality that all scrapers should implement.
"""

from abc import ABC, abstractmethod
from config.scrapers_config import ScraperConf
from datas.property_listing import PropertyListing
from network.http_client_handler import AsyncClientHandler
import logging
from typing import Optional
from core.url_discovery_strategy import URLDiscoveryStrategy

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """Base class for all scrapers."""
    
    def __init__(self, config:ScraperConf):
        """Initialize a basic scraper from the configuration

        Args:
            config (ScraperConf): Represents a configuration for a scraper with its details
        """
        self.scraper_name = config.get("name")
        self.enabled = config.get("enabled")
        self.crawler_strategy = config.get("scraper_type")
        self.base_url = config.get("startlink")
        self.url_strategy = config.get("url_strategy")
        self.client: Optional[AsyncClientHandler] = None
    
    @abstractmethod
    async def run(self):
        pass
    
    @abstractmethod
    async def get_data(self):
        pass
    
    @abstractmethod
    async def init_client(self):
        pass
    
    async def init_url_strategy(self) -> list[str]:
        strategy = URLDiscoveryStrategy(self.url_strategy)
        urls = await strategy.discover_urls(self.url_strategy, self.client)
        logger.info(
            f"[{self.scraper_name}] Trouvé {len(urls)} URLs dans le sitemap XML"
        )
        return urls
    
