# -*- coding: utf-8 -*-
"""
Base Scraper module.
This module provides a base class for scrapers, defining the common interface and functionnality that all scrapers should implement.
"""

from abc import ABC, abstractmethod
import asyncio
import inspect
from scrapling import Selector
from scrapling.fetchers import FetcherSession, AsyncStealthySession, AsyncDynamicSession
from config.squirrel_settings import PROXY, SIMPLE_TIMEOUT, ADVANCED_TIMEOUT, URL_PARSER_LIMITATION
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
        self.url_nb:None|int = URL_PARSER_LIMITATION # used to limit the number of URLs to be parsed
        self.scraper_name = config.get("scraper_name")
        self.enabled = config.get("enabled")
        self.crawler_strategy = config.get("scraper_type")
        self.start_link = config.get("start_link")
        self.url_strategy = config.get("url_strategy")
        self.selectors:SelectorFields = selectors
        self.listing:PropertyListing = PropertyListing(self.scraper_name)
    
    async def run(self) -> None:
        """Launch the scraper, discover url and scrape all the urls"""
        concurrency = 8
        # Discovery phase
        logger.info(f"[{self.scraper_name}] is starting to scrape data")
        urls = await self.url_discovery_strategy()
        if not urls:
            logger.warning("Cannot find any urls to be scraped")
            return None
        logger.info(f"[{self.scraper_name}] has discovered {len(urls)} urls to be scraped")

        if self.url_nb is not None:    
            target_urls = urls[:self.url_nb]
        else:
            target_urls = urls
        logger.info("[%s] %d URL to be scraped", self.scraper_name, len(target_urls))

        async with FetcherSession(timeout=SIMPLE_TIMEOUT, proxy=PROXY) as fetcher_session, AsyncDynamicSession(timeout=SIMPLE_TIMEOUT, proxy=PROXY, locale="fr-FR") as dynamic_session, AsyncStealthySession(timeout=ADVANCED_TIMEOUT, proxy=PROXY, geoip=True, solve_cloudflare=True, disable_ads=True, disable_resources=True, block_webrtc=True, block_images=True, os_randomize=True) as stealthy_session:
            sessions = (fetcher_session, dynamic_session, stealthy_session)
            sem = asyncio.Semaphore(concurrency) 

            async def worker(url: str) -> None:
                async with sem:
                    await self._scrape_one(url, sessions)

            tasks = [asyncio.create_task(worker(url)) for url in target_urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for url, result in zip(target_urls, results):
                if isinstance(result, Exception):
                    logger.error("Broken task for %s : %r", url, result)

        logger.info("[%s] scraping  is finished. %d properties collected ; %d fails.",
                    self.scraper_name,
                    self.listing.count_properties(),
                    len(getattr(self.listing, "failed_urls", [])))
    
    async def _scrape_one(self, url: str, sessions: tuple[FetcherSession, AsyncDynamicSession, AsyncStealthySession]) -> None:
        """
        Tente de scraper une URL avec retries par session, puis fallback sur la session suivante.
        Marque l’URL en échec si toutes les tentatives échouent.
        """
        retries = 2
        backoff_base = 0.8
        
        for session in sessions:
            for attempt in range(1, retries + 1):
                try:
                    html = await self._request(session, url)
                    property_ = await self.get_data(html, url)
                    if property_ is None:
                        raise ValueError("Returned property is None")

                    self.listing.add_property(property_)
                    logger.info("OK %s by %s (try %d/%d)",
                                url, type(session).__name__, attempt, 2)
                    return

                except Exception as exc:  # noqa: BLE001
                    backoff = (backoff_base ** attempt) * attempt
                    logger.warning(
                        "Failed %s by %s (try %d/%d) : %s — retry in %.2fs",
                        url, type(session).__name__, attempt, retries, exc, backoff
                    )
                    await asyncio.sleep(backoff)

            logger.info("Fallback on %s for %s", type(session).__name__, url)

        if not hasattr(self.listing, "failed_urls"):
            self.listing.failed_urls = []
        self.listing.failed_urls.append(url)
        logger.error("Surrender %s after all tries and backoff", url)
        
    async def _request(self, session: FetcherSession | AsyncDynamicSession | AsyncStealthySession, url: str) -> Selector:
        """Fetch a URL and return a Selector object.

        Args:
            url (str): The URL to fetch.
            session (FetcherSession | AsyncDynamicSession | AsyncStealthySession): The session to use for fetching.
        """
        fetch = getattr(session, "fetch", None)
        if fetch is not None:
            if inspect.iscoroutinefunction(fetch):
                return await fetch(url)

        get = getattr(session, "get", None)
        if get is None:
            raise AttributeError(
                f"La session {type(session).__name__} n’expose ni fetch() ni get()"
            )

        result = get(url)  # adding kwargs here : get(url, impersonate='firefox135')
        if inspect.isawaitable(result):
            return await result
        return result
        
    
    @abstractmethod
    async def get_data(self, page: Selector, url:str) -> Property | None:
        """Collect data from an HTML element
        
        Returns:
            Property | None: Represents a Property dataclass with all the data scraped or None if the scraper failed to scrape the data
        """
        pass
    
    @abstractmethod
    async def url_discovery_strategy(self) -> list[str]|None:
        """This method is used to collect the Urls to be scraped.
        It needs to be overwrite by some scrapers with non classic url discovery strategy like API and paginate URLs.

        Returns:
            list[str]|None: Represents list of urls to scrape or None if the program can't reach the start_link.
        """
        pass

    @classmethod
    def global_url_filter(cls, url:str|Selector) -> bool:
        """Add a url filter at the class level"""
        return True
    
    @abstractmethod
    def instance_url_filter(self, url:str|Selector) -> bool:
        """Overwrite to add a url filter at the instance level"""
        pass

    def filter_url(self, url:str|Selector) -> bool:
        """Return True if all filters are true."""
        return self.instance_url_filter(url) and BaseScraper.global_url_filter(url)


        
        
    
