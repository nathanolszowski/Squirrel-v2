# -*- coding: utf-8 -*-
"""
Scraper for BNP
"""

import logging
from core.http_scraper import VanillaScraper
from scrapling import Selector
from urllib.parse import urljoin
import json
import re
from config.scrapers_config import SCRAPER_CONFIG
from config.scrapers_selectors import SELECTORS
from config.squirrel_settings import DEPARTMENTS
from datas.property import Property

logger = logging.getLogger(__name__)

class BNPScraper(VanillaScraper):
    """CBRE scraper which inherits from VanillaHTTP class"""

    def __init__(self):
        super().__init__(SCRAPER_CONFIG["BNP"], SELECTORS["BNP"])

    def instance_url_filter(self, url:str|Selector) -> bool:
        """Overwrite to add a url filter at the instance level"""
        if "bureau" in url:
            if any(f"-{departement}/" in url for departement in DEPARTMENTS):
                return True
            else:
                return False
        else:
            return False

    async def data_hook(self, property:Property, page, url: str) -> None:
        """Post-processing hook method to be overwritten if necessary for specific datas in the Property dataclass

        Args:
            property (Property): Represent the data of the property to scrape
            page (Selector): Selector linked to the html page of the property to scrape
            url (str): Url of the property to scrape
        """
        # Contract
        if "a-louer" in url:
            property.contract = "Location"
            property.price = await self.select_text(self.selectors.get("global_rent"), page)
        elif "a-vendre" in url:
            property.contract = "Vente"
            property.price = await self.select_text(self.selectors.get("global_price"), page)
        else:
            property.contract = None
            
        # Asset type
        actif_map = {
            "bureau": "Bureaux",
            "local": "Locaux d'activité",
            "entrepot": "Entrepots",
            "coworking": "Bureau équipé",
        }
        property.asset_type = next(
            (label for key, label in actif_map.items() if key in url), None
        )
        # Adress concatenation
        adresse = await self.select_text(self.selectors.get("adress"), page)
        nom_immeuble = await self.select_text(self.selectors.get("building_name"), page)
        property.adress = f"{nom_immeuble} {adresse}".strip()

        # Image url
        parent_image = page.css_first("div.img-container img")

        if parent_image and parent_image.attrib["data-lazy"]:
            url_image = urljoin("https://www.bnppre.fr", parent_image.attrib["data-lazy"])
            property.url_image = url_image
        else:
            property.url_image = None


        # GPS
        script = page.css_first("script:contains('var geocode')")

        if script:
            script_text = script.text
            match = re.search(r"var geocode\s*=\s*(\{.*?\});", script_text, re.DOTALL)

            if match:
                geocode_json = match.group(1)
                geocode = json.loads(geocode_json)

                # Extraire la localisation
                location = geocode["results"][0]["geometry"]["location"]
                property.latitude = float(location["lat"])
                property.longitude = float(location["lng"])
            else:
                # fallback si pas de match
                property.latitude = 48.866669
                property.longitude = 2.33333
        else:
            property.latitude = 48.866669
            property.longitude = 2.33333