# -*- coding: utf-8 -*-
"""
Scrapers configuration
"""
from typing import Union, Dict, TypedDict

class ScraperConf(TypedDict):
    scraper_name:str
    enabled:bool
    scraper_type:str
    url_strategy:str
    start_link:Union[str, Dict[str, str]]


SCRAPER_CONFIG: Dict[str, ScraperConf] = {
    "BNP": {
        "scraper_name": "BNP",
        "enabled": True,
        "scraper_type": "HTTP",
        "url_strategy": "XML",
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
        "scraper_type": "PLAYWRIGHT",
        "url_strategy": "XML",
        "start_link": "https://immobilier.jll.fr/sitemap-properties.xml",
    },
    "CBRE": {
        "scraper_name": "CBRE",
        "enabled": True,
        "scraper_type": "HTTP",
        "url_strategy": "XML",
        "start_link": "https://immobilier.cbre.fr/sitemap.xml",
    },
    "ALEXBOLTON": {
        "scraper_name": "ALEXBOLTON",
        "enabled": True,
        "scraper_type": "HTTP",
        "url_strategy": "XML",
        "start_link": "https://immobilier.cbre.fr/sitemap.xml",
    },
    "CUSHMAN": {
        "scraper_name": "CUSHMAN",
        "enabled": True,
        "scraper_type": "HTTP",
        "url_strategy": "XML",
        "start_link": "https://immobilier.cushmanwakefield.fr/sitemap.xml",
    },
    "KNIGHTFRANK": {
        "scraper_name": "KNIGHTFRANK",
        "enabled": True,
        "scraper_type": "HTTP",
        "url_strategy": "URL",
        "start_link": {
            "Location": "https://www.knightfrank.fr/resultat?nature=1&localisation=75%7C77%7C78%7C91%7C92%7C93%7C94%7C95%7C&typeOffre=1",
            "Vente": "https://www.knightfrank.fr/resultat?nature=2&localisation=75%7C77%7C78%7C91%7C92%7C93%7C94%7C95%7C&typeOffre=1",
        },
    },
    "ARTHURLOYD": {
        "scraper_name": "ARTHURLOYD",
        "enabled": True,
        "scraper_type": "HTTP",
        "url_strategy": "XML",
        "start_link": "https://www.arthur-loyd.com/sitemap-offer.xml",
    },
    "SAVILLS": {
        "scraper_name": "SAVILLS",
        "enabled": True,
        "scraper_type": "API",
        "url_strategy": "API",
        "start_link": {
            "Bureaux_Location": "/fr/fr/liste?SearchList=Id_16+Category_RegionCountyCountry&Tenure=GRS_T_R&SortOrder=SO_PCDD&Currency=EUR&Period=Year&CommercialPropertyType=GRS_CPT_O&Receptions=-1&CommercialSizeUnit=SquareMeter&LandAreaUnit=SquareMeter&AvailableSizeUnit=SquareMeter&Category=GRS_CAT_COM&Shapes=W10",
            "Bureaux_Vente": "/fr/fr/liste?SearchList=Id_16+Category_RegionCountyCountry&Tenure=GRS_T_B&SortOrder=SO_PCDD&Currency=EUR&Period=Year&CommercialPropertyType=GRS_CPT_O&Receptions=-1&ResidentialSizeUnit=SquareMeter&CommercialSizeUnit=SquareMeter&LandAreaUnit=Acre&SaleableAreaUnit=SquareMeter&AvailableSizeUnit=SquareMeter&Category=GRS_CAT_COM&Shapes=W10",
            "Entrepots_Location": "/fr/fr/liste?SearchList=Id_1234+Category_RegionCountyCountry&Tenure=GRS_T_R&SortOrder=SO_PCDD&Currency=EUR&Period=Year&CommercialPropertyType=GRS_CPT_I&Receptions=-1&CommercialSizeUnit=SquareMeter&Category=GRS_CAT_COM&Shapes=W10",
            "Entrepots_Vente": "/fr/fr/liste?SearchList=Id_1234+Category_RegionCountyCountry&Tenure=GRS_T_B&SortOrder=SO_PCDD&Currency=EUR&Period=Year&CommercialPropertyType=GRS_CPT_I&Receptions=-1&ResidentialSizeUnit=SquareMeter&CommercialSizeUnit=SquareMeter&LandAreaUnit=Acre&SaleableAreaUnit=SquareMeter&AvailableSizeUnit=SquareMeter&Category=GRS_CAT_COM&Shapes=W10",
            "Coworking": "/fr/fr/liste?SearchList=Id_16+Category_RegionCountyCountry&Tenure=GRS_T_R&SortOrder=SO_PCDD&Currency=EUR&Period=Year&CommercialPropertyType=GRS_CPT_SO&Receptions=-1&CommercialSizeUnit=SquareFeet&LandAreaUnit=SquareFeet&AvailableSizeUnit=SquareFeet&Category=GRS_CAT_COM&Shapes=W10",
        },
    },
    # Add scrapers below
}
