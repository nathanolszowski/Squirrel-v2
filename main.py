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

    log_file = setup_logging()
    logger = logging.getLogger(__name__)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    scrapers = [CBREScraper()]
    logger.info(f"Starting scraping for scrapers {len(scrapers)}")
    for scraper in scrapers:
        try:
            logger.info(f"Starting scraping for {scraper.scraper_name} ...")
            await scraper.run()
            exporter = ListingExporter(scraper.listing)
            exporter.export_to_json("exports")
        except Exception as e:
            logger.error(f"Error when running the following scraper : {scraper.scraper_name} : {e}")

    logger.info(
        "Program finishing well"
    )

if __name__ == "__main__":
    asyncio.run(main())
