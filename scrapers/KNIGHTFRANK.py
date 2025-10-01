# -*- coding: utf-8 -*-
"""
Scraper for KNIGHT FRANK
"""

import logging
from core.http_scraper import HTTPScraper
from scrapling import Selector
from config.squirrel_settings import PROXY
from scrapling.fetchers import AsyncStealthySession, AsyncDynamicSession
import re
from config.scrapers_config import SCRAPER_CONFIG
from config.scrapers_selectors import SELECTORS
from config.squirrel_settings import DEPARTMENTS_IDF
from datas.property import Property

logger = logging.getLogger(__name__)

class KNIGHTFRANKScraper(HTTPScraper):
    """CBRE scraper which inherits from VanillaHTTP class"""

    def __init__(self):
        super().__init__(SCRAPER_CONFIG["KNIGHTFRANK"], SELECTORS["KNIGHTFRANK"])
        self.base_url = "https://www.knightfrank.fr"

    def instance_url_filter(self, url:str|Selector) -> bool:
        """Overwrite to add a url filter at the instance level"""
        return True

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
            (label for key, label in contrat_map.items() if key in url), "N/A"
        )
        # Asset type
        property.asset_type = "Bureaux"

        # Surcharger la méthode obtenir l'url image
        parent_image = page.css_first("div.col-xl-8 p-0 bg-dark photoUne img")
        if parent_image and parent_image.attrib["src"] :
            property.url_image = parent_image.attrib["src"] 
        # Surcharger la méthode obtenir la position
        scripts = page.css("script")
        for script in scripts:
            script_text = script.text()
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
                    
    async def _trouver_formater_urls_offres(self, page: Selector) -> list[str]:
        """Méthode qui permet de formater les urls KnightFrank lors de la méthode _navigation_page()

        Args:
            soup (BeautifulSoup): Représente le parser lié à la page html à scraper

        Returns:
            list[str]: Représente la liste d'urls formatées des offres à scraper
        """
        div_parent = page.css_first("#listCards > div")
        if not div_parent:
            logger.info("Pas d'élément listCards trouvé")
            return []
        else:
            offres = div_parent.css("div[class*='cardOffreListe']")
            liens = [offre.css_first("a.infosCard") for offre in offres if offre.css_first("a.infosCard")]
            hrefs = [
                self.base_url + lien.attrib["href"]
                for lien in liens
                if lien and lien.attrib["href"]
            ]
            return hrefs

    async def _navigation_page(self, url: str|None) -> list[str]|None:
        """Permet de naviguer entre les différentes pages d'offres

        Args:
            url (str): Représente la page HTML dans laquelle naviguer

        Returns:
            urls (list[str]): Représente la liste d'urls des offres à scraper
        """
        urls = []
        logger.info("Navigate through the pages to fetch all the offers urls")
        while url:
            logger.info(f"Fetching offers from page: {url}")
            
            urls += await self._trouver_formater_urls_offres()

            div_parent_page = page.css_first(
                "body > main > section > div.container.pagination.py-5 > div"
            )

            if div_parent_page:
                # Sélectionne tous les liens avec aria-label="Next"
                suivant = div_parent_page.css("a[aria-label='Next']")
                if suivant:
                    href = suivant[0].attrib["href"]
                    url = self.base_url + href
                else:
                    url = None
            else:
                url = None
        return urls

    async def url_discovery_strategy(self) -> list[str]|None:
        """
        This method overwrite the class method and it is used to collect the Urls to be scraped.

        Returns:
            list[str]|None: Represents list of urls to scrape or None if the program can't reach the start_link.
        """
        logger.info("Fetch urls from html page(s)")
        responses = []
        urls_discovery = []

        if isinstance(self.start_link, dict):
            logger.info("Fetching urls from multiple HTML pages")
            for actif, url in self.start_link.items():
                urls_discovery.append(url)
                logger.info(urls_discovery)
        else:
            logger.info("Fetching urls from a single HTML page")
            urls_discovery.append(self.start_link)

        for url in urls_discovery:
            response = await self._navigation_page(url)
            responses = response if response else []
        
        if responses:
            logger.info(f"{len(responses)} urls fetched from html page(s)")
            return responses
        else:
            logger.error("No url fetched from html page(s)")
            return None
