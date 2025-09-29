# -*- coding: utf-8 -*-
"""
HTTP Scraper module.
"""

from core.base_scraper import BaseScraper
import logging
from config.squirrel_settings import PROXY
from scrapling.fetchers import AsyncStealthySession, AsyncDynamicSession
from scrapling import Selector
from datas.property import Property
from config.scrapers_selectors import SelectorFields
from config.scrapers_config import ScraperConf

logger = logging.getLogger(__name__)

class HTTPScraper(BaseScraper):
    
    def __init__(self, config: ScraperConf, selectors:SelectorFields):
        super().__init__(config, selectors)
        
    async def run(self) -> None:
        """Launch the scraper, discover url and scrape all the urls"""
        logger.info(f"[{self.scraper_name}] is starting to scrape data")
        urls = await self.url_discovery_strategy()
        if not urls:
            logger.warning("Cannot find any urls to be scraped")
            return None
        
        # ====> Intégrer les requêteurs <====
        if self.url_nb is None :
            async with AsyncDynamicSession() as session:
                try:
                    for url in urls:
                        prop = await self.get_data(url)
                        if prop is not None:
                            self.listing.add_property(prop)
                except Exception as e:
                    self.listing.failed_urls.append(url)
                
        else:
            for url in urls[:self.url_nb]:
                prop = await self.get_data(url)
                if prop is not None:
                    self.listing.add_property(prop)
                else:
                    self.listing.failed_urls.append(url)
                    continue
        logger.info(f"[{self.scraper_name}] has finished scraping all the data : {self.listing.count_properties()}")
      
    async def get_data(self, page: Selector, url:str) -> Property | None:
        """Collect data from an HTML element
        
        Returns:
            Property | None: Represents a Property dataclass with all the data scraped or None if the scraper failed to scrape the data
        """
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
    
    def data_hook(self, property:Property, page: Selector, url:str) -> None:
        """Post-processing hook method to be overwritten if necessary for specific datas in the Property dataclass"""
        pass

    def instance_url_filter(self, url:str) -> bool:
        """Overwrite to add a url filter at the instance level"""
        return True




