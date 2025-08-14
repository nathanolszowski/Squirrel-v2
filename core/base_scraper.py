# -*- coding: utf-8 -*-
"""
Base Scraper module.
This module provides a base class for scrapers, defining the common interface and functionnality that all scrapers should implement.
"""

from abc import ABC, abstractmethod
from config.scrapers_config import ScraperConf
from datas.property_listing import PropertyListing
from selectolax.parser import HTMLParser
from datas.property import Property
from network.client_handler import HeadlessClientHandler, HTTPClientHandler
from config.scrapers_selectors import SelectorFields
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """Base class for all scrapers."""
    
    def __init__(self, config:ScraperConf, selectors:SelectorFields):
        """Initialize a basic scraper from the configuration

        Args:
            config (ScraperConf): Represents a configuration for a scraper with its details
        """
        self.url_nb:None|int = 5 # used to limit the number of URLs to scrape 
        self.scraper_name = config.get("scraper_name")
        self.enabled = config.get("enabled")
        self.crawler_strategy = config.get("scraper_type")
        self.start_link = config.get("start_link")
        self.url_strategy = config.get("url_strategy")
        self.client:Optional[HTTPClientHandler] = None
        self.browser:Optional[HeadlessClientHandler] = None
        self.selectors:SelectorFields = selectors
        self.listing:PropertyListing = PropertyListing(self.scraper_name)
    
    @abstractmethod
    async def run(self) -> None:
        """Launch the scraper, discover url and scrape all the urls"""
        pass
    
    @abstractmethod
    async def get_data(self, url: str) -> Property|None:
        """Collect data from an HTML page"""
        pass
    
    @abstractmethod
    async def init_client(self) -> None:
        """Initialize the http client for the actual scraper"""
        pass
    
    @abstractmethod
    def instance_url_filter(self, url:str):
        """Overwrite to add a url filter at the instance level"""
        pass

    @classmethod
    def global_url_filter(cls, url:str) -> bool:
        """Add a url filter at the class level"""
        return True

    def _filter_url(self, url:str) -> bool:
        """Retourne True si l'URL passe tous les filtres."""
        return self.instance_url_filter(url) and BaseScraper.global_url_filter(url)

    async def url_discovery_strategy(self) -> list[str]|None:
        """This method is used to collect the Urls to be scraped.
        It needs to be overwrite by some scrapers with non classic url discovery strategy like API and paginate URLs.

        Returns:
            list[str]|None: Represents list of urls to scrape or None if the program can't reach the start_link.
        """
        if self.client is not None:
            logger.info("Fetch urls from xml sitemap")
            failed_urls = []
            try:
                urls = []
                if isinstance(self.start_link, dict):
                    logger.info("Fetching urls from multiple sitemaps")
                    for actif, url in self.start_link.items():
                        response = await self.client.get(url)
                        if response is None:
                            logger.warning(f"No response from : {url}")
                            failed_urls.append(url)
                            continue
                        page = HTMLParser(response.text)
                        for node in page.css("url"):
                            loc_node = node.css_first("loc")
                            if loc_node and self._filter_url(loc_node.text()):
                                urls.append(loc_node.text())
                else:
                    logger.info("Fetching urls from a single sitemap")
                    response = await self.client.get(self.start_link)
                    if response is None:
                        logger.warning(f"No response from : {self.start_link}")
                        failed_urls.append(self.start_link)
                    else:
                        page = HTMLParser(response.text)
                        for node in page.css("url"):
                            loc_node = node.css_first("loc")
                            if loc_node and self._filter_url(loc_node.text()):
                                urls.append(loc_node.text())
                if failed_urls:
                    logger.warning(f"Sitemaps failed to load: {failed_urls}")
                logger.info(f"Sitemaps failed to load: {len(urls)}")
                return urls

            except Exception as e:
                logger.error(
                    f"Error when fetching urls for {self.scraper_name}: {e}"
                )
                return []
        
        
    
