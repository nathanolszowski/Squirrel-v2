# -*- coding: utf-8 -*-
"""
Scrapers configuration
"""
from enum import Enum
from typing import Union, Dict, List, Tuple


class ScraperType(str, Enum):
    HTTP = "HTTP"
    PW = "PLAYWRIGHT"
    API = "API"


class URLType(str, Enum):
    XML = "XML"
    URL = "URL"
    API = "API"


SCRAPER_CONFIG = {
    "BNP": {
        "enabled": True,
        "scraper_type": ScraperType.HTTP,
        "url_strategy": URLType.XML,
        "start_link": {
            "Bureaux": "https://www.bnppre.fr/sitemaps/bnppre/sitemap-bureaux.xml",
            "Coworking": "https://bnppre.fr/sitemaps/bnppre/sitemap-coworking.xml",
        },
        "filters": {"actif": "bureau", "region": "île-de-france"},
    },
    "JLL": {
        "enabled": False,
        "scraper_type": ScraperType.PW,
        "url_strategy": URLType.XML,
        "start_link": "https://immobilier.jll.fr/sitemap-properties.xml",
        "filters": {"actif": "bureau", "region": "île-de-france"},
    },
    "CBRE": {
        "enabled": True,
        "scraper_type": ScraperType.HTTP,
        "url_strategy": URLType.XML,
        "start_link": "https://immobilier.cbre.fr/sitemap.xml",
        "filters": {"actif": "bureau", "region": "île-de-france"},
    },
    "ALEXBOLTON": (URLType.XML, "https://www.alexbolton.fr/sitemap.xml"),
    "CUSHMAN": (URLType.XML, "https://immobilier.cushmanwakefield.fr/sitemap.xml"),
    "KNIGHTFRANK": (
        URLType.URL,
        {
            "Location": "https://www.knightfrank.fr/resultat?nature=1&localisation=75%7C77%7C78%7C91%7C92%7C93%7C94%7C95%7C&typeOffre=1",
            "Vente": "https://www.knightfrank.fr/resultat?nature=2&localisation=75%7C77%7C78%7C91%7C92%7C93%7C94%7C95%7C&typeOffre=1",
        },
    ),
    "ARTHURLOYD": (URLType.XML, "https://www.arthur-loyd.com/sitemap-offer.xml"),
    "SAVILLS": (
        URLType.API,
        {
            "Bureaux_Location": "/fr/fr/liste?Tenure=GRS_T_R&SortOrder=SO_PCDD&Currency=EUR&Period=Year&CommercialPropertyType=GRS_CPT_O&Receptions=-1&ResidentialSizeUnit=SquareMeter&CommercialSizeUnit=SquareMeter&LandAreaUnit=Acre&SaleableAreaUnit=SquareMeter&AvailableSizeUnit=SquareMeter&Category=GRS_CAT_COM&Shapes=W3sidHlwZSI6IkNpcmNsZSIsImNvb3JkaW5hdGVzIjpbMS40NDQyMDksNDMuNjA0NjUyXSwicmFkaXVzIjoiMjc4NzgwbSIsImxvY2F0aW9uSWQiOiI2MDcifV0",
            "Bureaux_Vente": "/fr/fr/liste?Tenure=GRS_T_B&SortOrder=SO_PCDD&Currency=EUR&Period=Year&CommercialPropertyType=GRS_CPT_O&Receptions=-1&ResidentialSizeUnit=SquareMeter&CommercialSizeUnit=SquareMeter&LandAreaUnit=Acre&SaleableAreaUnit=SquareMeter&AvailableSizeUnit=SquareMeter&Category=GRS_CAT_COM&Shapes=W3sidHlwZSI6IkNpcmNsZSIsImNvb3JkaW5hdGVzIjpbMS40NDQyMDksNDMuNjA0NjUyXSwicmFkaXVzIjoiMjc4NzgwbSIsImxvY2F0aW9uSWQiOiI2MDcifV0",
        },
    ),
    # Add scrapers below
}
