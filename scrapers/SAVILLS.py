# -*- coding: utf-8 -*-
"""
Scraper for SAVILLS
"""

import logging
from core.api_scraper import APIScraper
from scrapling import Selector
from config.scrapers_config import SCRAPER_CONFIG
from config.scrapers_selectors import SELECTORS
from config.squirrel_settings import DEPARTMENTS_IDF
from datas.property import Property

logger = logging.getLogger(__name__)

class SAVILLSScraper(APIScraper):
    """SAVILLS scraper which inherits from VanillaHTTP class"""

    def __init__(self):
        super().__init__(SCRAPER_CONFIG["SAVILLS"], None, "https://search.savills.com", "https://search.savills.com/fr/fr/bien-immobilier-details/", "https://livev6-searchapi.savills.com/Data/SearchByUrl")

    async def run(self)->None:
        """Launch the scraper, discover url and scrape all the urls"""
        header_search_url = {
            "gpscountrycode": "fr",
            "gpslanguagecode": "fr",
            "origin": self.base_url,
        }
        resultats = []
        # Pour chaque url de la liste de sitemap, récupérer le détail des offres
        for actif, url in self.start_link.items():
            page = 1
            nb_pages_resultats = 1
            while page <= nb_pages_resultats:
                params = f"{url}&Page={page}"
                params_url = {
                    "url": params,
                }
                try:
                    with httpx.Client(
                        proxy=self.proxy,
                        headers=header_search_url,
                        follow_redirects=True,
                        timeout=REQUEST_TIMEOUT,
                    ) as client:
                        reponse = client.post(self.api_url, data=params_url)
                    reponse.raise_for_status()
                    data = reponse.json()
                    # Extraire et sécuriser le nombre de pages
                    paging_info = (
                        data.get("Results", {}).get("PagingInfo", {}).get("PageCount")
                    )
                    if isinstance(paging_info, int) and paging_info > 0:
                        nb_pages_resultats = paging_info
                    else:
                        logger.warning(
                            f"[{self.scraper_name}] Aucune page trouvée pour {actif}"
                        )
                        break  # sortir de la boucle while

                    logger.info(
                        f"[{self.scraper_name}] Page {page} / {nb_pages_resultats} pour {actif}"
                    )
                    offres = data.get("Results", {}).get("Properties", [])
                    for offre in offres:
                        # Déterminer le type de contrat
                        contrat = offre.get("SizeDescription", "")
                        contrat_map = {
                            "louer": "Location",
                            "vendre": "Vente",
                        }
                        contrat = next(
                            (
                                label
                                for key, label in contrat_map.items()
                                if key in contrat
                            ),
                            "N/A",
                        )
                        # Déterminer le type d'actif
                        actif = offre.get("PropertyTypes", [{}])[0].get("Caption", "")
                        if (
                            isinstance(offre.get("PropertyTypes"), list)
                            and len(offre.get("PropertyTypes")) > 0
                        ):
                            if actif == "Entrepôts / Locaux d'activité":
                                for surface in offre.get("ByUnit"):
                                    type_surface = surface["Type"]
                                    if (
                                        type_surface == "Activités"
                                        or type_surface == "Entrepôts"
                                    ):
                                        actif = type_surface
                                        break
                        else:
                            actif = None

                        property = Property(
                            agency=self.scraper_name,
                            url= self.base_url_property
                            + offre.get("ExternalPropertyIDFormatted", ""),
                            reference= offre.get("ExternalPropertyIDFormatted", ""),
                            asset_type= actif,

                            contract = contrat,
                            disponibility= (
                                offre.get("ByUnit", [{}])[0].get("Disponibilité", "")
                                if isinstance(offre.get("ByUnit"), list)
                                and len(offre.get("ByUnit")) > 0
                                else ""
                            ),
                            area = offre.get("SizeFormatted", ""),
                            division = None,
                            adress = offre.get("AddressLine2", ""),
                            postal_code= None,
                            contact= offre.get("PrimaryAgent", {}).get(
                                "AgentName", ""),
                            resume= offre.get("Description", ""),
                            amenities= (
                                offre.get("LongDescription", [{}])[0].get("Body", "")
                                if isinstance(offre.get("LongDescription"), list)
                                and len(offre.get("LongDescription")) > 0 else None), 
                            url_image= offre.get("ImagesGallery")[0].get("ImageUrl_L", None),
                            latitude= offre.get("Latitude", ""),
                            longitude= offre.get("Longitude", ""),
                            price= offre.get("DisplayPriceText", ""),
                        )

                        self.listing.add_property(property)
                    page += 1

                except Exception as e:
                    logger.error(f"[{self.scraper_name}] Erreur page {page}: {e}")


    def instance_url_filter(self, url:str|Selector) -> bool:
        """Overwrite to add a url filter at the instance level"""
        return True

    async def data_hook(self, property:Property, page, url: str) -> None:
        """Post-processing hook method to be overwritten if necessary for specific datas in the Property dataclass

        Args:
            data (dict[str]): Représente les données de l'offre à scraper
            soup (BeautifulSoup): Représente le parser lié à la page html de l'offre à scraper
            url (str): Représente l'url de l'offre à scraper
        """
        pass