# -*- coding: utf-8 -*-
"""
HTTP Scraper module.
"""

from core.base_scraper import BaseScraper
import logging
import asyncio
from scrapling.fetchers import AsyncStealthySession, AsyncDynamicSession
from selectolax.parser import HTMLParser
from datas.property import Property
from config.scrapers_selectors import SelectorFields
from config.scrapers_config import ScraperConf
from config.squirrel_settings import PROXY


logger = logging.getLogger(__name__)

class HTTPScraper(BaseScraper):
    
    def __init__(self, config: ScraperConf, selectors:SelectorFields):
        super().__init__(config, selectors)
        
    async def run(self) -> None:
        """Launch the scraper, discover url and scrape all the urls"""
        pass
      
    async def get_data(self, url:str) -> Property|None:
        """Collect data from an HTML page"""
        pass
    
    def data_hook(self, property:Property, page, url:str) -> None:
        """Post-processing hook method to be overwritten if necessary for specific datas in the Property dataclass"""
        pass
    
    async def url_discovery_strategy(self) -> list[str]|None:
        logger.info("Fetch urls from xml sitemap")
        urls = []
        urls_discovery = []

        if isinstance(self.start_link, dict):
            logger.info("Fetching urls from multiple sitemaps")
            for actif, url in self.start_link.items():
                urls_discovery.append(url)
        else:
            logger.info("Fetching urls from a single sitemap")
            urls_discovery.append(self.start_link)

        responses = []
        # Utilise scrapling pour récupérer le contenu des sitemaps
        try:
            async with AsyncDynamicSession(proxy=PROXY, headless=False) as session:
                tasks = [session.fetch(url) for url in urls_discovery]
                responses = await asyncio.gather(*tasks)
        except Exception as e:
            logger.error(f"AsyncDynamicSession failed: {e}")
            try:
                async with AsyncStealthySession(proxy=PROXY, geoip=True) as session:
                    tasks = [session.fetch(url) for url in urls_discovery]
                    responses = await asyncio.gather(*tasks)
            except Exception as e:
                logger.error(f"AsyncStealthySession failed: {e}")
                responses = []

        # Parse chaque sitemap pour extraire les URLs
        logger.info(responses)
        for response in responses:
            if response is None or not hasattr(response, "text"):
                continue
            page = HTMLParser(response.text)
            for node in page.css("url"):
                loc_node = node.css_first("loc")
                if loc_node and self._filter_url(loc_node.text()):
                    urls.append(loc_node.text())
                    
        logger.info("Found %d urls to scrape", len(urls))
        return urls if urls else None
    
    def instance_url_filter(self, url:str) -> bool:
        """Overwrite to add a url filter at the instance level"""
        return True
  
class VanillaHTTP(HTTPScraper):
    
    def __init__(self, config: ScraperConf, selectors:SelectorFields):
        super().__init__(config, selectors)
        
    async def run(self) -> None:
        """Launch the scraper, discover url and scrape all the urls"""
        logger.info(f"[{self.scraper_name}] is starting to scrape data")
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
    
    async def get_data(self, url: str) -> Property | None:
        """Collect data from an HTML page using scrapling and selectolax, with fallback stealth session."""
        response = None
        try:
            async with AsyncDynamicSession(proxy=PROXY) as session:
                response = await session.fetch(url)
        except Exception as e:
            logger.error(f"[{self.scraper_name}] AsyncDynamicSession failed for {url}: {e}")
            try:
                async with AsyncStealthySession(proxy=PROXY, geoip=True) as session:
                    response = await session.fetch(url)
            except Exception as e:
                logger.error(f"[{self.scraper_name}] AsyncStealthySession failed for {url}: {e}")
                return None

        if response is None or not hasattr(response, "text"):
            return None

        page = HTMLParser(response.text)

        def select_text(selector):
            if selector:
                node = page.css_first(selector)
                return node.text(strip=True) if node else None
            return None

        property = Property(
            agency=self.scraper_name,
            url=url,
            reference=select_text(self.selectors.get("reference")),
            asset_type=select_text(self.selectors.get("asset_type")),
            contract=select_text(self.selectors.get("contract")),
            disponibility=select_text(self.selectors.get("disponibility")),
            area=select_text(self.selectors.get("area")),
            division=(
                select_text(self.selectors.get("division"))
                if self.selectors.get("division", None) is not None
                else "Non divisible"
            ),
            adress=select_text(self.selectors.get("adress")),
            postal_code=select_text(self.selectors.get("postal_code")),
            contact=select_text(self.selectors.get("contact")),
            resume=select_text(self.selectors.get("resume")),
            amenities=select_text(self.selectors.get("amenities")),
            url_image=select_text(self.selectors.get("url_image")),
            latitude=select_text(self.selectors.get("latitude")),
            longitude=select_text(self.selectors.get("longitude")),
            price=select_text(self.selectors.get("global_price")),
        )
        self.data_hook(property, page, url)
        return property
        
    
    def data_hook(self, property:Property, page, url:str) -> None:
        """Post-processing hook method to be overwritten if necessary for specific datas in the Property dataclass

        Args:
            data (dict[str]): Représente les données de l'offre à scraper
            soup (BeautifulSoup): Représente le parser lié à la page html de l'offre à scraper
            url (str): Représente l'url de l'offre à scraper
        """
        pass
    
    def instance_url_filter(self, url:str) -> bool:
        """Overwrite to add a url filter at the instance level"""
        return True
