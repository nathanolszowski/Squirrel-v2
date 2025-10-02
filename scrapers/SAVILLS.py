# -*- coding: utf-8 -*-
"""
Scraper for SAVILLS
"""

import logging
from core.api_scraper import APIScraper
from scrapling import Selector
import json
from urllib.parse import urlsplit, urlencode, parse_qsl, urlunsplit
from scrapling.fetchers import FetcherSession
from config.scrapers_config import SCRAPER_CONFIG
from config.scrapers_selectors import SELECTORS
from config.squirrel_settings import DEPARTMENTS_IDF, PROXY, SIMPLE_TIMEOUT
from datas.property import Property

logger = logging.getLogger(__name__)

class SAVILLSScraper(APIScraper):
    """SAVILLS scraper which inherits from VanillaHTTP class"""

    def __init__(self):
        super().__init__(SCRAPER_CONFIG["SAVILLS"], None, "https://search.savills.com", "https://search.savills.com/fr/fr/bien-immobilier-details/", "https://livev6-searchapi.savills.com/Data/SearchByUrl")

    def to_api_path(self, url: str, page: int) -> str:
        """
        Transforme une URL absolue/relative Savills en chemin + query
        attendu par l'API (ex: '/fr/fr/liste?...&Page=2').
        Ajoute/écrase le paramètre Page.
        """
        sp = urlsplit(url)
        # si url_base est déjà un chemin (commence par '/'), sp.scheme/host seront vides → OK
        query = dict(parse_qsl(sp.query, keep_blank_values=True))
        query["Page"] = str(page)
        # reconstruit uniquement path + query (l’API ne veut PAS le domaine)
        return urlunsplit(("", "", sp.path or url, urlencode(query, doseq=True), ""))
    
    async def run(self)->None:
        """Launch the scraper, discover url and scrape all the urls"""

        # self.start_link est un dict {actif: url_de_recherche}
        for actif_label, url_base in self.start_link.items():
            page: int = 1
            nb_pages_resultats: int = 1

            async with FetcherSession(
                proxy=PROXY,  # str type 'http://user:pass@host:port' accepté
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "gpscountrycode": "fr",
                    "gpslanguagecode": "fr",
                    "origin": self.base_url,
                },
                timeout=SIMPLE_TIMEOUT,
                stealthy_headers=True,
            ) as session:
                while page <= nb_pages_resultats:

                    body = {"url": self.to_api_path(url_base, page)}
                    try:
                        resp = await session.post(self.api_url, json=body)
                        data = resp.body
                        data_json = json.loads(data)

                        offres = (
                            data_json.get("Results", {}).get("Properties", []) or []
                        ) 
                        
                        for offre in offres:
                            size_desc = offre.get("SizeDescription", "") or ""
                            contrat_map = {"louer": "Location", "vendre": "Vente"}
                            contrat = next(
                                (label for key, label in contrat_map.items() if key in size_desc.lower()),
                                None,
                            )
                            # Type d'actif
                            actif = (
                                offre.get("PropertyTypes", [{}])[0].get("Caption", "")
                                if isinstance(offre.get("PropertyTypes"), list)
                                and offre.get("PropertyTypes")
                                else None
                            )
                            if actif == "Entrepôts / Locaux d'activité":
                                for surface in offre.get("ByUnit") or []:
                                    type_surface = surface.get("Type")
                                    if type_surface in {"Activités", "Entrepôts"}:
                                        actif = type_surface
                                        break

                            property = Property(
                                agency=self.scraper_name,
                                url=self.base_url_property
                                + (offre.get("ExternalPropertyIDFormatted", "") or ""),
                                reference=offre.get("ExternalPropertyIDFormatted", "") or "",
                                asset_type=actif,
                                contract=contrat,
                                disponibility=(
                                    (offre.get("ByUnit") or [{}])[0].get("Disponibilité", "")
                                    if isinstance(offre.get("ByUnit"), list)
                                    and len(offre.get("ByUnit")) > 0
                                    else ""
                                ),
                                area=offre.get("SizeFormatted", "") or None,
                                division=None,
                                adress=offre.get("AddressLine2", "") or None,
                                postal_code=None,
                                contact=(offre.get("PrimaryAgent", {}) or {}).get("AgentName", "") or "",
                                resume=offre.get("Description", "") or "",
                                amenities=(
                                    (offre.get("LongDescription") or [{}])[0].get("Body", "")
                                    if isinstance(offre.get("LongDescription"), list)
                                    and len(offre.get("LongDescription")) > 0
                                    else None
                                ),
                                url_image=(
                                    (offre.get("ImagesGallery") or [{}])[0].get("ImageUrl_L")
                                    if isinstance(offre.get("ImagesGallery"), list)
                                    and len(offre.get("ImagesGallery")) > 0
                                    else None
                                ),
                                latitude=offre.get("Latitude", "") or None,
                                longitude=offre.get("Longitude", "") or None,
                                price=offre.get("DisplayPriceText", "") or None,
                            )

                            self.listing.add_property(property)

                        # Nombre de pages
                        paging_info = (
                            data_json.get("Results", {})
                            .get("PagingInfo", {})
                            .get("PageCount")
                        )
                        if isinstance(paging_info, int) and paging_info > 0:
                            nb_pages_resultats = paging_info
                        else:
                            logger.warning(
                                "[%s] Aucune page trouvée pour %s",
                                self.scraper_name,
                                actif_label,
                            )
                            break

                        logger.info(
                            "[%s] Page %s / %s pour %s",
                            self.scraper_name,
                            page,
                            nb_pages_resultats,
                            actif_label,
                        )
                        page += 1

                    except Exception as exc:
                        logger.error("[%s] Erreur page %s: %s", self.scraper_name, page, exc)
                        break
        logger.info("[%s] scraping  is finished. %d properties collected",
                    self.scraper_name,
                    self.listing.count_properties())

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