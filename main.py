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
    for scraper in enabled_scrapers:
            try:
                logger.info(f"Starting scraping for {scraper.scraper_name} ...")
                await scraper.run()
                exporter = ListingExporter(scraper.listing)
                exporter.export_to_json("exports")
            except Exception as e:
                logger.error(f"Error when running the following scraper : {scraper.scraper_name} : {e}")

    logger.info(
        f"Program finishing properly, please check the log file {log_file} for details and the exported data in the folder exports",
    )

if __name__ == "__main__":
    asyncio.run(main())
