# -*- coding: utf-8 -*-
"""
Listing exporter class
"""

import json
from datas.property_listing import PropertyListing

class ListingExporter:
    """Exports property listings to various formats."""
    
    def __init__(self, data: PropertyListing):
        """Initializes the listing exporter."""
        self.exported_listings = data
        
    def export_to_json(self, path:str, fileobj=None):
        from dataclasses import asdict
        data = [asdict(prop) for prop in self.exported_listings.properties]
        if fileobj is None:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        else:
            json.dump(data, fileobj, ensure_ascii=False, indent=2)