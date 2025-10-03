# -*- coding: utf-8 -*-
"""
Scraper for CUSHMAN & WAKEFIELD
"""

import logging
from core.http_scraper import VanillaScraper
from scrapling import Selector
import re
import html
import json
from config.scrapers_config import SCRAPER_CONFIG
from config.scrapers_selectors import SELECTORS
from config.squirrel_settings import DEPARTMENTS
from datas.property import Property

logger = logging.getLogger(__name__)

class CUSHMANScraper(VanillaScraper):
    """CBRE scraper which inherits from VanillaHTTP class"""

    def __init__(self):
        super().__init__(SCRAPER_CONFIG["CUSHMAN"], SELECTORS["CUSHMANWAKEFIELD"])

    def instance_url_filter(self, url:str|Selector) -> bool:
        """Overwrite to add a url filter at the instance level"""
        pattern = re.compile(
            r"-\d{5}-\d+[a-zA-Z]*$"
        )  # chain format "-75009-139113AB"
        if pattern.search(url):
            if "bureaux" in url:
                last_segment = url.strip("/").split("/")[-1]
                part = last_segment.split("-")
                part = part[-2]
                if any(departement in part for departement in DEPARTMENTS):
                    return True
                else:
                    return False
            elif "activites" or "entrepots" in url:
                return True
            else:
                return False
        else:
            return False

    async def data_hook(self, property:Property, page, url: str) -> None:
        """Post-processing hook method to be overwritten if necessary for specific datas in the Property dataclass

        Args:
            data (dict[str]): Représente les données de l'offre à scraper
            soup (BeautifulSoup): Représente le parser lié à la page html de l'offre à scraper
            url (str): Représente l'url de l'offre à scraper
        """
        # Contract
        contrat_map = {"location": "Location", "achat": "Vente"}
        property.contract = next(
            (label for key, label in contrat_map.items() if key in url), "N/A"
        )
        
        # Asset type
        actif_map = {
            "bureaux": "Bureaux",
            "Bureaux": "Bureaux",
            "Activités": "Locaux d'activité",
            "Entrepôts": "Entrepots",
            "Coworking": "Bureau équipé",
            "Bureaux privés": "Bureau équipé",
        }
        property.asset_type = next(
            (label for key, label in actif_map.items() if key in property.asset_type), None
        )
        
        # Division
        if property.area is not None and "divisibles à partir" in property.area:
            divisible = property.area.find("divisibles")
            surface_divisible = property.area[:divisible].strip()
            divisibilite = property.area[divisible:].strip()
            property.area = surface_divisible
            property.division = divisibilite
        else:
            property.division = "Non divisibles"
        
        # Image url
        parent_image = page.css_first("div.c-swiper__slide source")
        if parent_image and parent_image.attrib["srcset"]:
            property.url_image = parent_image.attrib["srcset"]
        else:
            property.url_image = None
        # GPS position
        div_map = page.css_first("div.c-map.js-map")

        if div_map:
            data_property = div_map.attrib["data-property"]
            if data_property:
                decoded_json_str = html.unescape(data_property)
                positions = json.loads(decoded_json_str)

                property.latitude = float(
                    positions["address"]["displayedGeolocation"]["lat"]
                )
                property.longitude = float(
                    positions["address"]["displayedGeolocation"]["lon"]
                )
            else:
                property.latitude = 48.866669
                property.longitude = 2.33333
        else:
            property.latitude = 48.866669
            property.longitude = 2.33333
