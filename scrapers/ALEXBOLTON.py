# -*- coding: utf-8 -*-
"""
Scraper for ALEXBOLTON
"""

import logging
from core.http_scraper import HTTPScraper
from scrapling import Selector
from config.scrapers_config import SCRAPER_CONFIG
from config.squirrel_settings import DEPARTMENTS
from config.scrapers_selectors import SELECTORS
from datas.property import Property

logger = logging.getLogger(__name__)

class ALEXBOLTONScraper(HTTPScraper):
    """ALEXBOLTON scraper which inherits from VanillaHTTP class"""

    def __init__(self):
        super().__init__(SCRAPER_CONFIG["ALEXBOLTON"], SELECTORS["ALEXBOLTON"])

    def instance_url_filter(self, url:str|Selector) -> bool:
        """Overwrite to add a url filter at the instance level"""
        if url.startswith(
            "https://www.alexbolton.fr/annonces/"
        ) and any(departement in url for departement in DEPARTMENTS):
            return True
        else:
            return False

    async def data_hook(self, property:Property, page:Selector, url: str) -> None:
        """Post-processing hook method to be overwritten if necessary for specific datas in the Property dataclass

        Args:
            property (Property): Represent the data of the property to scrape
            page (Selector): Selector linked to the html page of the property to scrape
            url (str): Url of the property to scrape
        """
        property.asset_type = "Bureaux" # alexbolton only has office listings
        # Contract
        contrat_map = {
            "Loyer": "Location",
            "Prix": "Vente",
        }
        contract = await self.select_text(self.selectors.get("contract"), page)
        property.contract = next(
            (
                label
                for key, label in contrat_map.items()
                if key in contract
            ),
            None,
        )
        # Resume
        accroche_div = page.css_first("div.col-lg-5.position-relative")

        if accroche_div:
            paragraphs = accroche_div.css("p")
            for paragraph in paragraphs:  
                if len(paragraph.text) > 30:
                    property.resume = paragraph.text
                else:
                    property.resume = None
        else:
            property.resume = None
        # Amenities
        amenities_div = page.css_first("div.listing-details-description.mb-3")
        amenities_list = amenities_div.css("p::text")
        if amenities_div:
            property.amenities = amenities_list
        else:
            property.amenities = None
            
        # Image url
        img = page.css_first("img.listing-header-photo-img.u-z-index-1.d-md-none")

        if img:
            src = img.attrib["src"]
            if src:
                property.url_image = src
            else:
                property.url_image = None
        else:
            property.url_image = None
        
        # GPS position
        position_div = page.css_first("div#listing-map-target")

        if position_div:
            lat = position_div.attrib["data-latitude"]
            lon = position_div.attrib["data-longitude"]

            if lat and lon:
                property.latitude = float(lat)
                property.longitude = float(lon)
            else:
                property.latitude = 48.866669
                property.longitude = 2.33333
        else:
            property.latitude = 48.866669
            property.longitude = 2.33333
        