# -*- coding: utf-8 -*-
"""
Scraper for ARTHURLOYD
"""

import logging
from core.http_scraper import VanillaScraper
from urllib.parse import urljoin
import json
import html
from scrapling import Selector
from config.scrapers_config import SCRAPER_CONFIG
from config.scrapers_selectors import SELECTORS
from config.squirrel_settings import DEPARTMENTS
from datas.property import Property

logger = logging.getLogger(__name__)

class ARTHURLOYDScraper(VanillaScraper):
    """CBRE scraper which inherits from VanillaHTTP class"""

    def __init__(self):
        super().__init__(SCRAPER_CONFIG["ARTHURLOYD"], SELECTORS["ARTHURLOYD"])

    def instance_url_filter(self, url:str|Selector) -> bool:
        """Overwrite to add a url filter at the instance level"""
        motifs_url = [
            "bureau-location/",
            "bureau-vente/",
            "locaux-activite-entrepots-location/",
            "locaux-activite-entrepots-vente/",
            "logistique-location/",
            "logistique-vente/",
        ]
        if any(motif in url for motif in motifs_url) and any(departement in url for departement in DEPARTMENTS):
            return True
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
        contrat_map = {
            "location": "Location",
            "vente": "Vente",
        }
        property.contract = next(
            (label for key, label in contrat_map.items() if key in url), None
        )
        # Asset type
        actif_map = {
            "bureau": "Bureaux",
            "activite-entrepots": "Locaux d'activité",
            "logistique": "Entrepots",
        }
        property.asset_type = next(
            (label for key, label in actif_map.items() if key in url), None
        )
        # Url image
        li = page.css_first("#ogallery li")
        if li:
            property.url_image = urljoin(
                "https://www.arthur-loyd.com", li.attrib["data-background"]
            )
        # GPS position
        div = page.css_first("div[data-live-props-value]")

        if div:
            encoded_data = div.attrib.get("data-live-props-value")
            if encoded_data:
                decoded_data = html.unescape(encoded_data)
                data_dict = json.loads(decoded_data)

                markers = data_dict.get("markers", [])
                if markers:
                    property.latitude = float(markers[0].get("latitude"))
                    property.longitude = float(markers[0].get("longitude"))
                else:
                    property.latitude = 48.866669
                    property.longitude = 2.33333
            else:
                property.latitude = 48.866669
                property.longitude = 2.33333
        else:
            property.latitude = 48.866669
            property.longitude = 2.33333