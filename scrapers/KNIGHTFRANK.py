# -*- coding: utf-8 -*-
"""
Scraper for KNIGHT FRANK
"""

import logging
from core.http_scraper import HTTPScraper
from scrapling import Selector
from config.scrapers_config import SCRAPER_CONFIG
from config.scrapers_selectors import SELECTORS
from config.squirrel_settings import DEPARTMENTS_IDF
from datas.property import Property

logger = logging.getLogger(__name__)

class KNIGHTFRANKScraper(HTTPScraper):
    """CBRE scraper which inherits from VanillaHTTP class"""

    def __init__(self):
        super().__init__(SCRAPER_CONFIG["KNIGHTFRANK"], SELECTORS["KNIGHTFRANK"])

    def instance_url_filter(self, url:str|Selector) -> bool:
        """Overwrite to add a url filter at the instance level"""
        return True

    async def data_hook(self, property:Property, page, url: str) -> None:
        """Post-processing hook method to be overwritten if necessary for specific datas in the Property dataclass

        Args:
            data (dict[str]): Représente les données de l'offre à scraper
            soup (BeautifulSoup): Représente le parser lié à la page html de l'offre à scraper
            url (str): Représente l'url de l'offre à scraper
        """
        pass