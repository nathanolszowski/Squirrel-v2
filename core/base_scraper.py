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
from selectolax.parser import HTMLParser
from typing import Optional

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
    
    async def url_discovery_strategy(self) -> list[str]:
        if self.client is not None:
            logger.info("Fetch urls from xml sitemap")
            failed_urls = []
            try:
                urls = []
                if isinstance(self.base_url, dict):
                    logger.info("Fetching urls from multiple sitemaps")
                    for actif, url in self.base_url.items():
                        async with self.client as client:
                            response = await client.get(url)
                        if response is None:
                            logger.warning(f"No response from : {url}")
                            failed_urls.append(url)
                            continue
                        page = HTMLParser(response.text)
                        for node in page.css("url"):
                            loc_node = node.css_first("loc")
                            if loc_node:
                                urls.append(loc_node.text())
                else:
                    logger.info("Fetching urls from a single sitemap")
                    async with self.client as client:
                        response = await client.get(self.base_url)
                        if response is None:
                            logger.warning(f"No response from : {self.base_url}")
                            failed_urls.append(self.base_url)
                        else:
                            page = HTMLParser(response.text)
                            for node in page.css("url"):
                                loc_node = node.css_first("loc")
                                if loc_node:
                                    urls.append(loc_node.text())
                if failed_urls:
                    logger.warning(f"Sitemaps failed to load: {failed_urls}")
                return urls

            except Exception as e:
                logger.error(
                    f"Error when fetching urls from {self.base_url}: {e}"
                )
                return []
        
        
    
