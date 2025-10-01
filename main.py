# -*- coding: utf-8 -*-
"""
Main program
"""

from utils.logging import setup_logging
from scrapers.CBRE import CBREScraper
from scrapers.JLL import JLLScraper
from scrapers.BNP import BNPScraper
from scrapers.ARTHURLOYD import ARTHURLOYDScraper
from scrapers.SAVILLS import SAVILLSScraper
from scrapers.KNIGHTFRANK import KNIGHTFRANKScraper
from scrapers.CUSHMAN import CUSHMANScraper
from datas.listing_manager import ListingManager
from datas.listing_exporter import ListingExporter
import logging
import asyncio

async def main():
    """Fonction principale"""

    log_file = setup_logging()
    logger = logging.getLogger(__name__)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    scrapers = [CBREScraper(), BNPScraper(), JLLScraper(), ARTHURLOYDScraper(), SAVILLSScraper(), KNIGHTFRANKScraper(), CUSHMANScraper()]
    enabled_scrapers = [scraper for scraper in scrapers if scraper.enabled]
    logger.info(f"Starting scraping for scrapers {len(enabled_scrapers)} / {len(scrapers)} enabled : {[scraper.scraper_name for scraper in enabled_scrapers]}")
    listing_manager = ListingManager()
    for scraper in enabled_scrapers:
            try:
                logger.info(f"Starting scraping for {scraper.scraper_name} ...")
                await scraper.run()
                listing_manager.add_listing(scraper.listing)
            except Exception as e:
                logger.error(f"Error when running the following scraper : {scraper.scraper_name} : {e}")
    exporter = ListingExporter(listing_manager)
    exporter.export_to_json("exports")

    logger.info(
        f"Program finishing properly, please check the log file {log_file} for details and the exported data in the folder exports",
    )

if __name__ == "__main__":
    asyncio.run(main())
