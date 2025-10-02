# -*- coding: utf-8 -*-
"""
API Scraper module.
"""

from core.base_scraper import BaseScraper
from datas.property import Property
from scrapling import Selector
import logging

logger = logging.getLogger(__name__)

class APIScraper(BaseScraper):
    
    def __init__(self, config, selectors, base_url, base_url_property, api_url):
        super().__init__(config, selectors)
        self.base_url:str = base_url
        self.base_url_property:str = base_url_property
        self.api_url:str = api_url

    async def run(self) -> None:
        """Launch the scraper, discover url and scrape all the urls"""
        pass
    
    async def get_data(self, page: Selector, url: str) -> Property|None:
        """Collect data from an HTML page"""
        pass
    
    async def url_discovery_strategy(self) -> list[str]|None:
        """This method is used to collect the Urls to be scraped.
        It needs to be overwrite by some scrapers with non classic url discovery strategy like API and paginate URLs.

        Returns:
            list[str]|None: Represents list of urls to scrape or None if the program can't reach the start_link.
        """
        pass
    
    def instance_url_filter(self, url:str) -> bool:
        """Overwrite to add a url filter at the instance level"""
        return True

