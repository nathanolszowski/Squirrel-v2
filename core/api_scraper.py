# -*- coding: utf-8 -*-
"""
API Scraper module.
"""

from base_scraper import BaseScraper
from datas.property import Property
from network.client_handler import HTTPClientHandler
import logging

logger = logging.getLogger(__name__)

class APIScraper(BaseScraper):
    
    def __init__(self, config, selectors, base_url, base_url_property, api_url):
        super().__init__(config, selectors)
        self.base_url = base_url
        self.base_url_property = base_url_property
        self.api_url = api_url

    async def run(self) -> None:
        """Launch the scraper, discover url and scrape all the urls"""
        pass
    
    async def get_data(self, url: str) -> Property|None:
        """Collect data from an HTML page"""
        pass
    
    async def init_client(self) -> None:
        """Initialize the http client for the actual scraper"""
        pass
    
    def instance_url_filter(self, url:str):
        """Overwrite to add a url filter at the instance level"""
        pass

class VanillaAPI(APIScraper):

    def __init__(self, config, selectors, base_url, base_url_property, api_url):
        super().__init__(config, selectors, base_url, base_url_property, api_url)

    async def run(self) -> None:
        """Launch the scraper, discover url and scrape all the urls"""
        pass

    async def init_client(self) -> None:
        """Initialize the http client for the actual scraper"""
        self.client = HTTPClientHandler()
        await self.client.setup_client()

    async def get_data(self, url: str) -> Property|None:
        """Collect data from an HTML page"""
        pass

    def instance_url_filter(self, url:str):
        """Overwrite to add a url filter at the instance level"""
        pass