# -*- coding: utf-8 -*-
"""
Listing exporter class
"""

import json
from datas.listing_manager import ListingManager
from datas.property_listing import PropertyListing

class ListingExporter:
    """Exports property listings to various formats."""
    
    def __init__(self, data: PropertyListing):
        """Initializes the listing exporter."""
        self.exported_listings = data
        
    def export_to_json(self, path:str):
        from dataclasses import asdict
        with open(path, "w", encoding="utf-8") as f:
            json.dump([asdict(prop) for prop in self.exported_listings.properties], f, ensure_ascii=False, indent=2)