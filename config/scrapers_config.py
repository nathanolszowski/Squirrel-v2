# -*- coding: utf-8 -*-
"""
Scrapers configuration
"""
from typing import Dict, TypedDict

class ScraperConf(TypedDict):
    scraper_name:str
    enabled:bool
    start_link:str|dict[str, str]


SCRAPER_CONFIG: Dict[str, ScraperConf] = {
    "BNP": {
        "scraper_name": "BNP",
        "enabled": False,
        "start_link": {
            "Bureaux": "https://www.bnppre.fr/sitemaps/bnppre/sitemap-bureaux.xml",
            "Entrepot": "https://www.bnppre.fr/sitemaps/bnppre/sitemap-entrepots.xml",
            "Activite": "https://www.bnppre.fr/sitemaps/bnppre/sitemap-locaux.xml",
            "Coworking": "https://bnppre.fr/sitemaps/bnppre/sitemap-coworking.xml",
        },
    },
    "JLL": {
        "scraper_name": "JLL",
        "enabled": False,
        "start_link": "https://immobilier.jll.fr/sitemap-properties.xml",
    },
    "CBRE": {
        "scraper_name": "CBRE",
        "enabled": True,
        "start_link": "https://immobilier.cbre.fr/sitemap.xml",
    },
    "ALEXBOLTON": {
        "scraper_name": "ALEXBOLTON",
        "enabled": False,
        "start_link": "https://www.alexbolton.fr/sitemap.xml",
    },
    "CUSHMAN": {
        "scraper_name": "CUSHMAN",
        "enabled": False,
        "start_link": "https://immobilier.cushmanwakefield.fr/sitemap.xml",
    },
    "KNIGHTFRANK": {
        "scraper_name": "KNIGHTFRANK",
        "enabled": True,
        "start_link": "https://www.knightfrank.fr/sitemap.xml"
    },
    "ARTHURLOYD": {
        "scraper_name": "ARTHURLOYD",
        "enabled": False,
        "start_link": "https://www.arthur-loyd.com/sitemap-offer.xml",
    },
    "SAVILLS": {
        "scraper_name": "SAVILLS",
        "enabled": False,
        "start_link": {
            "Bureaux_Location": "/fr/fr/liste?SearchList=Id_16+Category_RegionCountyCountry&Tenure=GRS_T_R&SortOrder=SO_PCDD&Currency=EUR&Period=Year&CommercialPropertyType=GRS_CPT_O&Receptions=-1&CommercialSizeUnit=SquareMeter&LandAreaUnit=SquareMeter&AvailableSizeUnit=SquareMeter&Category=GRS_CAT_COM&Shapes=W10",
            "Bureaux_Vente": "/fr/fr/liste?SearchList=Id_16+Category_RegionCountyCountry&Tenure=GRS_T_B&SortOrder=SO_PCDD&Currency=EUR&Period=Year&CommercialPropertyType=GRS_CPT_O&Receptions=-1&ResidentialSizeUnit=SquareMeter&CommercialSizeUnit=SquareMeter&LandAreaUnit=Acre&SaleableAreaUnit=SquareMeter&AvailableSizeUnit=SquareMeter&Category=GRS_CAT_COM&Shapes=W10",
            "Entrepots_Location": "/fr/fr/liste?SearchList=Id_1234+Category_RegionCountyCountry&Tenure=GRS_T_R&SortOrder=SO_PCDD&Currency=EUR&Period=Year&CommercialPropertyType=GRS_CPT_I&Receptions=-1&CommercialSizeUnit=SquareMeter&Category=GRS_CAT_COM&Shapes=W10",
            "Entrepots_Vente": "/fr/fr/liste?SearchList=Id_1234+Category_RegionCountyCountry&Tenure=GRS_T_B&SortOrder=SO_PCDD&Currency=EUR&Period=Year&CommercialPropertyType=GRS_CPT_I&Receptions=-1&ResidentialSizeUnit=SquareMeter&CommercialSizeUnit=SquareMeter&LandAreaUnit=Acre&SaleableAreaUnit=SquareMeter&AvailableSizeUnit=SquareMeter&Category=GRS_CAT_COM&Shapes=W10",
            "Coworking": "/fr/fr/liste?SearchList=Id_16+Category_RegionCountyCountry&Tenure=GRS_T_R&SortOrder=SO_PCDD&Currency=EUR&Period=Year&CommercialPropertyType=GRS_CPT_SO&Receptions=-1&CommercialSizeUnit=SquareFeet&LandAreaUnit=SquareFeet&AvailableSizeUnit=SquareFeet&Category=GRS_CAT_COM&Shapes=W10",
        },
    },
}
"""
    "SCRAPER_NAME": {
    "scraper_name": "SCRAPER_NAME",
    "enabled": True|False,
    "start_link": "URL",
},
"""
