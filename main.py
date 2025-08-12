# -*- coding: utf-8 -*-
"""
Main program
"""

from utils.logging import setup_logging
from scrapers.CBRE import CBREScraper
from datas.listing_exporter import ListingExporter
import logging
import asyncio

async def main():
    """Fonction principale"""

    # Logging configuration
    log_file = setup_logging()
    logger = logging.getLogger(__name__)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    # Scrapers list
    scrapers = [CBREScraper()]
    logger.info("Starting scraping for scrapers")
    for scraper in scrapers:
        try:
            logger.info(f"Starting scraping for {scraper.scraper_name} ...")
            await scraper.run()
            exporter = ListingExporter()
            logger.info(f"Scraping results {scraper.listing.count_properties()}")
            exporter.export_to_json(scraper.listing)
        except Exception as e:
            logger.error(f"Erorr {scraper.scraper_name} : {e}")

    logger.info(
        "Program ending well"
    )

if __name__ == "__main__":
    asyncio.run(main())
