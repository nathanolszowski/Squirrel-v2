# -*- coding: utf-8 -*-
"""
HTTP Scraper module.
"""

from base_scraper import BaseScraper
import logging
from selectolax.parser import HTMLParser
from typing import Any
from datas.property import Property
from network.client_handler import HTTPClientHandler, HeadlessClientHandler
from config.scrapers_selectors import SelectorFields
from config.scrapers_config import ScraperConf

logger = logging.getLogger(__name__)

class HTTPScraper(BaseScraper):
    
    def __init__(self, config: ScraperConf, selectors:SelectorFields):
        super().__init__(config, selectors)
        
    async def init_client(self) -> None:
        """Initialize the http client for the actual scraper"""
        pass
        
    async def run(self) -> None:
        """Launch the scraper, discover url and scrape all the urls"""
        pass
      
    async def get_data(self, url:str) -> Property|None:
        """Collect data from an HTML page"""
        pass
    
    def data_hook(self) -> None:
        """Post-processing hook method to be overwritten if necessary for specific datas in the Property dataclass"""
        pass
  
class VanillaHTTP(HTTPScraper):
    
    def __init__(self, config: ScraperConf, selectors:SelectorFields):
        super().__init__(config, selectors)
        
    async def init_client(self) -> None:
        """Initialize the http client for the actual scraper"""
        self.client = HTTPClientHandler()
        await self.client.setup_client()
        
    async def run(self) -> None:
        """Launch the scraper, discover url and scrape all the urls"""
        logger.info(f"[{self.scraper_name}] is starting to scrape data")
        await self.init_client()
        urls = await self.url_discovery_strategy()
        if not urls:
            logger.warning("Cannot find any urls to be scraped")
            return
        if self.url_nb is None :
            for url in urls:
                prop = await self.get_data(url)
                if prop is not None:
                    self.listing.add_property(prop)
                else:
                    self.listing.failed_urls.append(url)
                    continue
        else:
            for url in urls[:self.url_nb]:
                prop = await self.get_data(url)
                if prop is not None:
                    self.listing.add_property(prop)
                else:
                    self.listing.failed_urls.append(url)
                    continue
        logger.info(f"[{self.scraper_name}] has finished scraping all the data : {self.listing.count_properties}")

    async def get_data(self, url:str) -> Property|None:
        """Collect data from an HTML page"""
        if self.client is not None:
            try:
                async with self.client as client:
                    response = await client.get(url)
            except Exception as e:
                logger.error(f"[{self.scraper_name}] Enable to fetch {url} to get data: {e}")
            else:
                if response is None:
                    return None
                page = HTMLParser(response.text)
                property = Property(
                    agency=self.scraper_name,
                    url=url,
                    reference=self.safe_select_text(page, self.selectors.get("reference")),
                    contract=self.safe_select_text(page, self.selectors.get("contract")),
                    active=self.safe_select_text(page, self.selectors.get("active")),
                    disponibility=self.safe_select_text(page, self.selectors.get("disponibility")),
                    area=self.safe_select_text(page, self.selectors.get("area")),
                    division=(
                        self.safe_select_text(page, self.selectors.get("division"))
                        if self.selectors.get("division", None) is not None
                        else "Non divisible"
                    ),
                    adress=self.safe_select_text(page, self.selectors.get("adress")),
                    postal_code=self.safe_select_text(page, self.selectors.get("postal_code", None)),
                    contact=self.safe_select_text(page, self.selectors.get("contact")),
                    resume=self.safe_select_text(page, self.selectors.get("resume")),
                    amenities=self.safe_select_text(page, self.selectors.get("amenities")),
                    url_image=self.safe_select_text(page, self.selectors.get("url_image")),
                    latitude=self.safe_select_text(page, self.selectors.get("latitude")),
                    longitude=self.safe_select_text(page, self.selectors.get("longitude")),
                    price=self.safe_select_text(page, self.selectors.get("global_price")),
                )
                return property
    
    def data_hook(self) -> None:
        """Post-processing hook method to be overwritten if necessary for specific datas in the Property dataclass"""
        pass
    
    def safe_select_text(self, tree:HTMLParser, selector:str|None) -> Any:
        """
        Extract text from an HTML element securely from a Selectolax tree.

        Args:
            tree (HTMLParser): HTML tree parsed by selectolax
            selector (str): CSS selector from settings.py
        Returns:
            (str): Selector text value else None
        """
        if selector is None:
            return None
        try:
            node = tree.css_first(selector)
            return node.text(strip=True) if node else None
        except Exception as e:
            logger.error(
                f"[{self.scraper_name}] Error with the following css selector='{selector}': {e}"
            )
            return None

class PlaywrightScraper(HTTPScraper):

    def __init__(self, config: ScraperConf, selectors:SelectorFields):
        super().__init__(config, selectors)
        
    async def run(self) -> None:
        """Launch the scraper, discover url and scrape all the urls"""
        # mode browser default + browser camoufox
        pass
    
    async def get_data(self, url:str) -> Property|None:
        """Collect data from an HTML page"""
        pass
    
    def data_hook(self) -> None:
        """Post-processing hook method to be overwritten if necessary for specific datas in the Property dataclass"""
        pass