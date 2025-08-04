# -*- coding: utf-8 -*-
"""
Base Scraper module.
This module provides a base class for scrapers, defining the common interface and functionnality that all scrapers should implement.
"""

from abc import ABC, abstractmethod
from config.scrapers_config import SCRAPER_CONFIG, ScraperConf
from typing import Dict

class BaseScraper(ABC):
    """Base class for all scrapers."""
    
    def __init__(self, config: Dict[str, ScraperConf]):
        self.scraper_name = config.get("name")
        self.base_url
        self.source_type
        self.crawler_strategy
        self.url_strategy
        self.navigator
        
    async def run(self):
        await self.init_client()
        data = await self.get_data()
        return data
    
    @abstractmethod
    async def get_data(self):
        pass
    
    @abstractmethod
    async def init_client(self) -> None:
        pass