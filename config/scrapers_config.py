# -*- coding: utf-8 -*-
"""
Scrapers configuration
"""
from enum import Enum
from typing import Union, Dict, List, Tuple, TypedDict


class ScraperType(str, Enum):
    HTTP = "HTTP"
    PW = "PLAYWRIGHT"
    API = "API"


class URLType(str, Enum):
    XML = "XML"
    URL = "URL"
    API = "API"


class ScraperConf(TypedDict):
    enabled: bool
    scraper_type: ScraperType
    url_strategy: URLType
    start_link: Union[str, Dict[str, str]]
    filters: Dict[str, Dict[str, str]]


DEFAULT_FILTERS = {
    "surface": {"field": "actif", "value": ["bureau"], "mode": "equal"},
    "localisation": {
        "field": "localisation",
        "value": ["idf", "paris"],
        "mode": "contains",
    },
}

SCRAPER_CONFIG: Dict[str, ScraperConf] = {
    "BNP": {
        "enabled": True,
        "scraper_type": ScraperType.HTTP,
        "url_strategy": URLType.XML,
        "start_link": {
            "Bureaux": "https://www.bnppre.fr/sitemaps/bnppre/sitemap-bureaux.xml",
            "Coworking": "https://bnppre.fr/sitemaps/bnppre/sitemap-coworking.xml",
        },
        "filters": DEFAULT_FILTERS,
    },
    "JLL": {
        "enabled": False,
        "scraper_type": ScraperType.PW,
        "url_strategy": URLType.XML,
        "start_link": "https://immobilier.jll.fr/sitemap-properties.xml",
        "filters": DEFAULT_FILTERS,
    },
    "CBRE": {
        "enabled": True,
        "scraper_type": ScraperType.HTTP,
        "url_strategy": URLType.XML,
        "start_link": "https://immobilier.cbre.fr/sitemap.xml",
        "filters": DEFAULT_FILTERS,
    },
    "ALEXBOLTON": {
        "enabled": True,
        "scraper_type": ScraperType.HTTP,
        "url_strategy": URLType.XML,
        "start_link": "https://immobilier.cbre.fr/sitemap.xml",
        "filters": DEFAULT_FILTERS,
    },
    "CUSHMAN": {
        "enabled": True,
        "scraper_type": ScraperType.HTTP,
        "url_strategy": URLType.XML,
        "start_link": "https://immobilier.cushmanwakefield.fr/sitemap.xml",
        "filters": DEFAULT_FILTERS,
    },
    "KNIGHTFRANK": {
        "enabled": True,
        "scraper_type": ScraperType.HTTP,
        "url_strategy": URLType.URL,
        "start_link": {
            "Location": "https://www.knightfrank.fr/resultat?nature=1&localisation=75%7C77%7C78%7C91%7C92%7C93%7C94%7C95%7C&typeOffre=1",
            "Vente": "https://www.knightfrank.fr/resultat?nature=2&localisation=75%7C77%7C78%7C91%7C92%7C93%7C94%7C95%7C&typeOffre=1",
        },
        "filters": DEFAULT_FILTERS,
    },
    "ARTHURLOYD": {
        "enabled": True,
        "scraper_type": ScraperType.HTTP,
        "url_strategy": URLType.XML,
        "start_link": "https://www.arthur-loyd.com/sitemap-offer.xml",
        "filters": DEFAULT_FILTERS,
    },
    "SAVILLS": {
        "enabled": True,
        "scraper_type": ScraperType.API,
        "url_strategy": URLType.API,
        "start_link": {
            "Bureaux_Location": "/fr/fr/liste?Tenure=GRS_T_R&SortOrder=SO_PCDD&Currency=EUR&Period=Year&CommercialPropertyType=GRS_CPT_O&Receptions=-1&ResidentialSizeUnit=SquareMeter&CommercialSizeUnit=SquareMeter&LandAreaUnit=Acre&SaleableAreaUnit=SquareMeter&AvailableSizeUnit=SquareMeter&Category=GRS_CAT_COM&Shapes=W3sidHlwZSI6IkNpcmNsZSIsImNvb3JkaW5hdGVzIjpbMS40NDQyMDksNDMuNjA0NjUyXSwicmFkaXVzIjoiMjc4NzgwbSIsImxvY2F0aW9uSWQiOiI2MDcifV0",
            "Bureaux_Vente": "/fr/fr/liste?Tenure=GRS_T_B&SortOrder=SO_PCDD&Currency=EUR&Period=Year&CommercialPropertyType=GRS_CPT_O&Receptions=-1&ResidentialSizeUnit=SquareMeter&CommercialSizeUnit=SquareMeter&LandAreaUnit=Acre&SaleableAreaUnit=SquareMeter&AvailableSizeUnit=SquareMeter&Category=GRS_CAT_COM&Shapes=W3sidHlwZSI6IkNpcmNsZSIsImNvb3JkaW5hdGVzIjpbMS40NDQyMDksNDMuNjA0NjUyXSwicmFkaXVzIjoiMjc4NzgwbSIsImxvY2F0aW9uSWQiOiI2MDcifV0",
        },
        "filters": DEFAULT_FILTERS,
    },
    # Add scrapers below
}
