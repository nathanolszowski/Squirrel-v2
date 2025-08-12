# -*- coding: utf-8 -*-
"""
HTTP Scraper module.
"""

from core.base_scraper import BaseScraper
import logging
from typing import Any
from datas.property import Property
from selectolax.parser import HTMLParser
from network.client_handler import HTTPClientHandler, HeadlessClientHandler
from config.scrapers_selectors import SelectorFields
from config.scrapers_config import ScraperConf
from playwright.sync_api import Page

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
    
    def instance_url_filter(self, url:str):
        """Overwrite to add a url filter at the instance level"""
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

    def instance_url_filter(self, url:str):
        """Overwrite to add a url filter at the instance level"""
        pass
    
    async def get_data(self, url:str) -> Property|None:
        """Collect data from an HTML page"""
        await self.init_client()
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
                    asset_type=self.safe_select_text(page, self.selectors.get("asset_type")),
                    contract=self.safe_select_text(page, self.selectors.get("contract")),
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
                self.data_hook(property, page, url)
                return property
    
    def data_hook(self, property:Property, page:HTMLParser, url:str) -> None:
        """Post-processing hook method to be overwritten if necessary for specific datas in the Property dataclass

        Args:
            data (dict[str]): Représente les données de l'offre à scraper
            soup (BeautifulSoup): Représente le parser lié à la page html de l'offre à scraper
            url (str): Représente l'url de l'offre à scraper
        """
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

    def __init__(self, config:ScraperConf, selectors:SelectorFields):
        super().__init__(config, selectors)
        
    async def init_client(self) -> None:
        """Initialize the http client for the actual scraper"""
        self.client = HTTPClientHandler()
        await self.client.setup_client()
        self.browser = HeadlessClientHandler()
        await self.browser.setup_client()
        
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
        logger.info(f"[{self.scraper_name}] has finished scraping all the data : {self.listing.count_properties()}")
        
    def instance_url_filter(self, url:str):
        """Overwrite to add a url filter at the instance level"""
        pass
    
    async def get_data(self, url:str) -> Property|None:
        """Collect data from an Playwright Page

        Args:
            url (str): Url of the resource to scrape

        Returns:
            Property|None: Property object with its details or None
        """
        if self.browser is not None:
            try:
                async with self.browser as client:
                    if client.context is not None:
                        page = client.context.new_page()
                        response = await page.goto(url)
                    else:
                        page = client.browser.new_page()
                        response = await page.goto(url)
            except Exception as e:
                logger.error(f"[{self.scraper_name}] Enable to fetch {url} to get data: {e}")
            else:
                if response is None:
                    return None
                
                latitude_str = await self.safe_select_text(page, self.selectors.get("latitude"))
                latitude = float(latitude_str) if latitude_str not in (None, "") else None
                longitude_str = await self.safe_select_text(page, self.selectors.get("longitude"))
                longitude = float(longitude_str) if longitude_str not in (None, "") else None
                
                property = Property(
                    agency=self.scraper_name,
                    url=url,
                    reference=await self.safe_select_text(page, self.selectors.get("reference")),
                    asset_type=await self.safe_select_text(page, self.selectors.get("asset_type")),
                    contract=await self.safe_select_text(page, self.selectors.get("contract")),
                    disponibility=await self.safe_select_text(page, self.selectors.get("disponibility")),
                    area=await self.safe_select_text(page, self.selectors.get("area")),
                    division=(
                        await self.safe_select_text(page, self.selectors.get("division"))
                        if self.selectors.get("division") is not None
                        else "Non divisible"
                    ),
                    adress=await self.safe_select_text(page, self.selectors.get("adress")),
                    postal_code=await self.safe_select_text(page, self.selectors.get("postal_code")),
                    contact=await self.safe_select_text(page, self.selectors.get("contact")),
                    resume=await self.safe_select_text(page, self.selectors.get("resume")),
                    amenities=await self.safe_select_text(page, self.selectors.get("amenities")),
                    url_image=await self.safe_select_text(page, self.selectors.get("url_image")),
                    latitude=latitude,
                    longitude=longitude,
                    price=await self.safe_select_text(page, self.selectors.get("global_price")),
                )
                return property

    async def safe_select_text(self, page:Page, selector: str | None) -> str | None:
        """Extract text from an HTML element securely with Playwright.

        Args:
            page (Page): Playwright page object
            selector (str | None): CSS selector from the config

        Returns:
            str | None: Extracted text or None
        """
        if selector is None:
            return None
        try:
            locator = page.locator(selector)
            if await locator.count() == 0:
                return None
            text = await locator.text_content()
            return text.strip() if text else None
        except Exception as e:
            logger.error(
                f"[{self.scraper_name}] Error with selector '{selector}': {e}"
            )
            return None
        
    def data_hook(self, property:Property, page: HTMLParser, url: str) -> None:
        """Post-processing hook method to be overwritten if necessary for specific datas in the Property dataclass

        Args:
            data (dict[str]): Représente les données de l'offre à scraper
            soup (BeautifulSoup): Représente le parser lié à la page html de l'offre à scraper
            url (str): Représente l'url de l'offre à scraper
        """
        pass