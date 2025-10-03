# -*- coding: utf-8 -*-
"""
HTTP Scraper module.
"""

from core.base_scraper import BaseScraper
import logging
from config.squirrel_settings import PROXY, ADVANCED_TIMEOUT
from typing import Any
from scrapling.fetchers import AsyncStealthySession, AsyncDynamicSession
from scrapling import Selector
from datas.property import Property
from config.scrapers_selectors import SelectorFields
from config.scrapers_config import ScraperConf

logger = logging.getLogger(__name__)

class VanillaScraper(BaseScraper):
    
    def __init__(self, config: ScraperConf, selectors:SelectorFields):
        super().__init__(config, selectors)
        
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
            async with AsyncDynamicSession(proxy=PROXY) as session:
                for url in urls_discovery:
                    page = await session.fetch(url)
                    response = page.xpath('//url/loc/text()')
                    for url in response:
                        if self.filter_url(url):
                            responses.append(url)
        except Exception as e:
            logger.error(f"AsyncDynamicSession failed: {e}")
            try:
                async with AsyncStealthySession(timeout=ADVANCED_TIMEOUT, proxy=PROXY, geoip=True, solve_cloudflare=True, disable_ads=True, disable_resources=True, block_webrtc=True, block_images=True, os_randomize=True) as session:
                    for url in urls_discovery:
                        page = await session.fetch(url)
                        response = page.xpath('//url/loc/text()')
                        for url in response:
                            if self.filter_url(url):
                                responses.append(url)
            except Exception as e:
                logger.error(f"AsyncStealthySession failed: {e}")
                logger.warning("Both sessions failed to fetch the sitemap(s)")
                return None
        else:
            logger.info(f"Successfully fetched {len(responses)} urls from the sitemap(s)")
            return responses
        
    async def select_text(self, selector, page:Selector) -> Any|None:
        """Helper function to select text from a selector"""
        if selector is not None:
            node = page.css_first(selector)
            return node.text if node else None
        else:
            return None
        
    async def get_data(self, page: Selector, url:str) -> Property | None:
        """Collect data from an HTML element
        
        Returns:
            Property | None: Represents a Property dataclass with all the data scraped or None if the scraper failed to scrape the data
        """
        property = Property(
            agency=self.scraper_name,
            url=url,
            reference=await self.select_text(self.selectors.get("reference"), page),
            asset_type=await self.select_text(self.selectors.get("asset_type"), page),
            contract=await self.select_text(self.selectors.get("contract"), page),
            disponibility=await self.select_text(self.selectors.get("disponibility"), page),
            area=await self.select_text(self.selectors.get("area"), page),
            division=(
                await self.select_text(self.selectors.get("division"), page)
                if self.selectors.get("division", None) is not None
                else "Non divisible"
            ),
            adress= await self.select_text(self.selectors.get("adress"), page),
            postal_code= await self.select_text(self.selectors.get("postal_code"), page),
            contact= await self.select_text(self.selectors.get("contact"), page),
            resume= await self.select_text(self.selectors.get("resume"), page),
            amenities= await self.select_text(self.selectors.get("amenities"), page),
            url_image= await self.select_text(self.selectors.get("url_image"), page),
            latitude= await self.select_text(self.selectors.get("latitude"), page),
            longitude= await self.select_text(self.selectors.get("longitude"), page),
            price= await self.select_text(self.selectors.get("global_price"), page),
        )
        await self.data_hook(property, page, url)
        return property
    
    async def data_hook(self, property:Property, page:Selector, url:str) -> None:
        """Post-processing hook method to be overwritten if necessary for specific datas in the Property dataclass"""
        pass

    def instance_url_filter(self, url:str) -> bool:
        """Overwrite to add a url filter at the instance level"""
        return True




