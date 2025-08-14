# -*- coding: utf-8 -*-
"""
Scraper for CBRE
"""

import logging
from core.http_scraper import PlaywrightScraper
from config.scrapers_config import SCRAPER_CONFIG
from config.scrapers_selectors import SELECTORS
from config.squirrel_settings import DEPARTMENTS_IDF
from datas.property import Property

logger = logging.getLogger(__name__)

class JLLScraper(PlaywrightScraper):
    """CBRE scraper which inherits from VanillaHTTP class"""

    def __init__(self):
        super().__init__(SCRAPER_CONFIG["JLL"], SELECTORS["JLL"])