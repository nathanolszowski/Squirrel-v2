# -*- coding: utf-8 -*-
"""
Listing exporter class
"""
from datas.listing_manager import ListingManager
class ListingExporter:
    """Exports property listings to various formats."""
    
    def __init__(self):
        """Initializes the listing exporter."""
        self.exported_listings: dict = {}
        
    def export_to_json(self):
        pass