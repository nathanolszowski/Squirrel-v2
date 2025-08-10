# -*- coding: utf-8 -*-
"""
Scraper for CBRE
"""

import logging
import re
from core.http_scraper import VanillaHTTP
from config.scrapers_config import SCRAPER_CONFIG
from config.scrapers_selectors import SELECTORS
from config.squirrel_settings import DEPARTMENTS_IDF

logger = logging.getLogger(__name__)

class CBREScraper(VanillaHTTP):
    """CBRE scraper which inherits from VanillaHTTP class"""

    def __init__(self):
        super().__init__(SCRAPER_CONFIG["CBRE"], SELECTORS["CBRE"])

    def instance_url_filter(self, url:str) -> bool:
        """Overwrite to add a url filter at the instance level"""
        logger.info("URL filter for cbre")
        pattern = re.compile(
            r"https://immobilier.cbre.fr/offre/(a-louer|a-vendre)/(bureaux|coworking)/(\d+)"
        )
        if url.startswith(
            "https://immobilier.cbre.fr/offre/"
        ):  # On filtre les offres bureaux dont l'url commence par cette string
            if "bureaux" in url:
                match = pattern.match(url)
                if match and match.group(2)[:2] in DEPARTMENTS_IDF:
                    return True
            else:
                logger.info(
                    f"[{url}] Url not to be scraped"
                )
                return False
        logger.info(
            f"[{url}] Url to be scraped"
        )

    def data_hook(self) -> None:
        """Post-processing hook method to be overwritten if necessary for specific datas in the Property dataclass

        Args:
            data (dict[str]): Représente les données de l'offre à scraper
            soup (BeautifulSoup): Représente le parser lié à la page html de l'offre à scraper
            url (str): Représente l'url de l'offre à scraper
        """
        # Surcharger la méthode obtenir la reference
        reference_element = soup.find("li", class_="LS breadcrumb-item active")
        reference_element = reference_element.find("span")
        data["reference"] = (
            reference_element.get_text(strip=True) if reference_element else "N/A"
        )
        # Surcharger la méthode obtenir l'actif
        actif_map = {
            "bureaux": "Bureaux",
            "activites": "Locaux d'activité",
            "entrepots": "Entrepots",
            "coworking": "Bureau équipé",
        }
        data["actif"] = next(
            (label for key, label in actif_map.items() if key in url), "N/A"
        )
        # Surcharger la méthode obtenir le contrat
        contrat_map = {
            "a-louer": "Location",
            "a-vendre": "Vente",
        }
        data["contrat"] = next(
            (label for key, label in contrat_map.items() if key in url), "N/A"
        )
        # Surcharger la méthode obtenir l'url image
        parent_image = soup.find("div", class_="main-image")
        img_image = parent_image.find("img")
        if img_image and img_image["src"]:
            data["url_image"] = img_image["src"]

        # Surcharger la méthode obtenir la position gps
        parent = soup.find("a", id="contentHolder_streetMapLink")
        if parent:
            href = parent.get("href")
            match = re.search(r"cbll=([\d\.]+),([\d\.]+)", href)
            if match:
                data["latitude"] = float(match.group(1))
                data["longitude"] = float(match.group(2))
            else:
                data["latitude"] = 48.866669
                data["longitude"] = 2.33333
        else:
            data["latitude"] = 48.866669
            data["longitude"] = 2.33333