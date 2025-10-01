# -*- coding: utf-8 -*-
"""
Listing exporter class
"""

import json
import os
from datetime import datetime
from datas.listing_manager import ListingManager

class ListingExporter:
    """Exports property listings to various formats."""
    
    def __init__(self, data:ListingManager):
        """Initializes the listing exporter."""
        self.exported_listings = data
        
    def export_to_json(self, path:str, fileobj=None):
        if not os.path.exists(path):
            os.makedirs(path)
        now = datetime.now().strftime("%Y-%m-%d_%H-%M")
        log_file = os.path.join(path, f"{now}.json")
        data = self.exported_listings.get_flat_dict()
        if fileobj is None:
            with open(log_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        else:
            json.dump(data, fileobj, ensure_ascii=False, indent=2)