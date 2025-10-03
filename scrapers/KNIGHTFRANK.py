# -*- coding: utf-8 -*-
"""
Scraper for KNIGHT FRANK
"""

import logging
from core.http_scraper import HTTPScraper
from scrapling import Selector
import re
from config.scrapers_config import SCRAPER_CONFIG
from config.scrapers_selectors import SELECTORS
from config.squirrel_settings import DEPARTMENTS
from datas.property import Property

logger = logging.getLogger(__name__)

class KNIGHTFRANKScraper(HTTPScraper):
    """CBRE scraper which inherits from VanillaHTTP class"""

    def __init__(self):
        super().__init__(SCRAPER_CONFIG["KNIGHTFRANK"], SELECTORS["KNIGHTFRANK"])
        self.base_url = "https://www.knightfrank.fr"

    def instance_url_filter(self, url:str|Selector) -> bool:
        """Overwrite to add a url filter at the instance level"""
        if url.startswith("https://www.knightfrank.fr/annonce/"):
            return True
        else:
            return False

    async def data_hook(self, property:Property, page, url: str) -> None:
        """Post-processing hook method to be overwritten if necessary for specific datas in the Property dataclass

        Args:
            property (Property): Represent the data of the property to scrape
            page (Selector): Selector linked to the html page of the property to scrape
            url (str): Url of the property to scrap
        """
        # Contract
        contrat_map = {
            "location": "Location",
            "vente": "Vente",
        }
        property.contract = next(
            (label for key, label in contrat_map.items() if key in url), None
        )
        # Asset type
        property.asset_type = "Bureaux"

        # Url image
        parent_image = page.css_first("div.col-xl-8 p-0 bg-dark photoUne img")
        if parent_image and parent_image.attrib["src"] :
            property.url_image = parent_image.attrib["src"] 

        # Surcharger la méthode obtenir la position
        scripts = page.css("script")
        for script in scripts:
            script_text = script.text
            if script_text and "initMap" in script_text:  # Filtrer le script contenant initMap
                lat_match = re.search(r"lat\s*:\s*([0-9\.\-]+)", script_text)
                lng_match = re.search(r"lng\s*:\s*([0-9\.\-]+)", script_text)

                if lat_match and lng_match:
                    property.latitude = float(lat_match.group(1))
                    property.longitude = float(lng_match.group(1))
                    break
                else:
                    property.latitude = 48.866669
                    property.longitude = 2.33333
            else:
                property.latitude = 48.866669
                property.longitude = 2.33333
     

                        
