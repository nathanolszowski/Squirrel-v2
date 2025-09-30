# -*- coding: utf-8 -*-
"""
Scraper for CBRE
"""

import logging
from scrapling import Selector
from core.http_scraper import HTTPScraper
from config.scrapers_config import SCRAPER_CONFIG
from config.scrapers_selectors import SELECTORS
from config.squirrel_settings import DEPARTMENTS_IDF
from datas.property import Property

logger = logging.getLogger(__name__)

class JLLScraper(HTTPScraper):
    """JLL scraper which inherits from VanillaHTTP class"""

    def __init__(self):
        super().__init__(SCRAPER_CONFIG["JLL"], SELECTORS["JLL"])
        
    def instance_url_filter(self, url:str|Selector) -> bool:
        """Overwrite to add a url filter at the instance level"""
        if url.startswith("https://immobilier.jll.fr/location") or url.startswith(
            "https://immobilier.jll.fr/vente"
        ):
            if "bureaux" or "coworking" in url:
                last_segment = url.strip("/").split("/")[-1]
                part = last_segment.split("-")
                part = part[-2]
                if any(departement in part for departement in DEPARTMENTS_IDF):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    async def data_hook(self, property:Property, page:Selector, url: str) -> None:
        """Post-processing hook method to be overwritten if necessary for specific datas in the Property dataclass

        Args:
            property (Property): Represent the data of the property to scrape
            page (Selector): Selector linked to the html page of the property to scrape
            url (str): Url of the property to scrape
        """
        contrat_map = {
            "a-louer": "Location",
            "a-vendre": "Vente",
        }
        property.contract = next(
            (label for key, label in contrat_map.items() if key in url), None
        )
        # Surcharger la méthode obtenir le contrat
        actif_map = {
            "bureaux": "Bureaux",
            "local-activite": "Locaux d'activité",
            "entrepot": "Entrepots",
        }
        property.asset_type = next(
            (label for key, label in actif_map.items() if key in url), None
        )