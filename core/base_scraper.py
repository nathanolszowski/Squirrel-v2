# -*- coding: utf-8 -*-
"""
Base Scraper module.
This module provides a base class for scrapers, defining the common interface and functionnality that all scrapers should implement.
"""

from abc import ABC, abstractmethod
from scrapling import Selector
from scrapling.fetchers import AsyncStealthySession, AsyncDynamicSession
from config.squirrel_settings import PROXY
from config.scrapers_config import ScraperConf
from datas.property_listing import PropertyListing
from datas.property import Property
from config.scrapers_selectors import SelectorFields
import logging

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """Base class for all scrapers."""
    
    def __init__(self, config:ScraperConf, selectors:SelectorFields):
        """Initialize a basic scraper from the configuration

        Args:
            config (ScraperConf): Represents a configuration for a scraper with its details
        """
        self.url_nb:None|int = 5 # used to limit the number of URLs to be scraped
        self.scraper_name = config.get("scraper_name")
        self.enabled = config.get("enabled")
        self.crawler_strategy = config.get("scraper_type")
        self.start_link = config.get("start_link")
        self.url_strategy = config.get("url_strategy")
        self.selectors:SelectorFields = selectors
        self.listing:PropertyListing = PropertyListing(self.scraper_name)
    
    @abstractmethod
    async def run(self) -> None:
        """Launch the scraper, discover url and scrape all the urls"""
        pass
    
    @abstractmethod
    async def get_data(self, page: Selector, url:str) -> Property | None:
        """Collect data from an HTML element
        
        Returns:
            Property | None: Represents a Property dataclass with all the data scraped or None if the scraper failed to scrape the data
        """
        pass
    
    async def url_discovery_strategy(self) -> list[str]|None:
        """This method is used to collect the Urls to be scraped.
        It needs to be overwrite by some scrapers with non classic url discovery strategy like API and paginate URLs.

        Returns:
            list[str]|None: Represents list of urls to scrape or None if the program can't reach the start_link.
        """
        logger.info("Fetch urls from xml sitemap")
        responses = []
        urls_discovery = []

        if isinstance(self.start_link, dict):
            logger.info("Fetching urls from multiple sitemaps")
            for actif, url in self.start_link.items():
                urls_discovery.append(url)
        else:
            logger.info("Fetching urls from a single sitemap")
            urls_discovery.append(self.start_link)

        try:
            async with AsyncDynamicSession() as session:
                for url in urls_discovery:
                    page = await session.fetch(url)
                    responses.append(loc for loc in page.xpath('//url/loc/text()'))
        except Exception as e:
            logger.error(f"AsyncDynamicSession failed: {e}")
            try:
                async with AsyncStealthySession() as session:
                    for url in urls_discovery:
                        page = await session.fetch(url)
                        responses.append(loc for loc in page.xpath('//url/loc/text()'))
            except Exception as e:
                logger.error(f"AsyncStealthySession failed: {e}")
        else:
            logger.info(f"Successfully fetched {len(responses)} sitemaps")

    @classmethod
    def global_url_filter(cls, url:str) -> bool:
        """Add a url filter at the class level"""
        return True
    
    @abstractmethod
    def instance_url_filter(self, url:str) -> bool:
        """Overwrite to add a url filter at the instance level"""
        pass

    def filter_url(self, url:str) -> bool:
        """Return True if all filters are true."""
        return self.instance_url_filter(url) and BaseScraper.global_url_filter(url)


        
        
    
