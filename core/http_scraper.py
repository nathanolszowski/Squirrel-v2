# -*- coding: utf-8 -*-
"""
HTTP Scraper module.
"""

from core.base_scraper import BaseScraper
import logging
from scrapling.fetchers import FetcherSession, DynamicSession, StealthySession
from datas.property import Property
from config.scrapers_selectors import SelectorFields
from config.scrapers_config import ScraperConf


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
    
    def data_hook(self, property:Property, url:str) -> None:
        """Post-processing hook method to be overwritten if necessary for specific datas in the Property dataclass"""
        pass

    async def url_discovery_strategy(self) -> list[str]|None:
        """This method is used to collect the Urls to be scraped.
        It needs to be overwrite by some scrapers with non classic url discovery strategy like API and paginate URLs.

        Returns:
            list[str]|None: Represents list of urls to scrape or None if the program can't reach the start_link.
        """
        logger.info("Fetch urls from xml sitemap")
        failed_urls = []
        try:
            urls = []
            if isinstance(self.start_link, dict):
                logger.info("Fetching urls from multiple sitemaps")
                for actif, url in self.start_link.items():
                    async with FetcherSession(impersonate='chrome') as session:
                        page = session.get(url)
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
    
    async def get_data(self, url:str) -> Property|None:
        """Collect data from an HTML page"""
        if self.client is not None:
            try:
                response = await self.client.get(url)
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
    
    def data_hook(self, property:Property, url:str) -> None:
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
