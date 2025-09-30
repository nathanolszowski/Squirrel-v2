# -*- coding: utf-8 -*-
"""
Scraper for CBRE
"""

import logging
import re
from core.http_scraper import HTTPScraper
from scrapling import Selector
from config.scrapers_config import SCRAPER_CONFIG
from config.scrapers_selectors import SELECTORS
from config.squirrel_settings import DEPARTMENTS_IDF
from datas.property import Property

logger = logging.getLogger(__name__)

class CBREScraper(HTTPScraper):
    """CBRE scraper which inherits from VanillaHTTP class"""

    def __init__(self):
        super().__init__(SCRAPER_CONFIG["CBRE"], SELECTORS["CBRE"])

    def instance_url_filter(self, url:str|Selector) -> bool:
        """Overwrite to add a url filter at the instance level"""
        pattern = re.compile(
            r"https://immobilier\.cbre\.fr/offre/(a-louer|a-vendre)/(bureaux|coworking)/(\d+)"
        )
        url = str(url)
        if not url.startswith("https://immobilier.cbre.fr/offre/"):
            return False

        match = pattern.match(url)
        if match:
            department_code = match.group(3)[:2]
            if department_code in DEPARTMENTS_IDF:
                return True
            else:
                return False
        else:
            return False


    def data_hook(self, property:Property, page, url: str) -> None:
        """Post-processing hook method to be overwritten if necessary for specific datas in the Property dataclass

        Args:
            data (dict[str]): Représente les données de l'offre à scraper
            soup (BeautifulSoup): Représente le parser lié à la page html de l'offre à scraper
            url (str): Représente l'url de l'offre à scraper
        """
        # Référence
        reference_element = page.css_first("li.LS.breadcrumb-item.active span")
        property.reference = reference_element.text(strip=True) if reference_element else "N/A"

        # Actif
        actif_map = {
            "bureaux": "Bureaux",
            "activites": "Locaux d'activité",
            "entrepots": "Entrepots",
            "coworking": "Bureau équipé",
        }
        property.asset_type = next((label for key, label in actif_map.items() if key in url), "N/A")

        # Contrat
        contrat_map = {
            "a-louer": "Location",
            "a-vendre": "Vente",
        }
        property.contract = next((label for key, label in contrat_map.items() if key in url), "N/A")

        # URL image
        img_image = page.css_first("div.main-image img")
        if img_image and img_image.attributes.get("src"):
            property.url_image = img_image.attributes["src"]

        # Position GPS
        parent = page.css_first("a#contentHolder_streetMapLink")
        if parent:
            href = parent.attributes.get("href", "")
            if isinstance(href, str):
                match = re.search(r"cbll=([\d\.]+),([\d\.]+)", href)
                if match:
                    property.latitude = float(match.group(1))
                    property.longitude = float(match.group(2))
                else:
                    property.latitude = 48.866669
                    property.longitude = 2.33333
        else:
            property.latitude = 48.866669
            property.longitude = 2.33333