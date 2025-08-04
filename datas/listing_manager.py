# -*- coding: utf-8 -*-
"""
Listing manager class
"""

from datas.property_listing import PropertyListing
from datas.property import Property

class ListingManager:
    """Manages the property listings."""
    
    def __init__(self):
        """Initializes the listing manager."""
        self.listings: dict[str, PropertyListing] = {}
        
    def add_listing(self, name_agency_listing: str) -> PropertyListing:
        """Adds a new property listing to the manager.
        
        Returns:
            listing (PropertyListing): The created property listing instance.
        """
        listing = PropertyListing(name_agency_listing)
        self.listings[name_agency_listing] = listing
        return listing
    
    def get_all_properties(self) -> list[Property]:
        """Returns all properties from all listings.
        
        Returns:
            properties (list[Property]): A list of all properties across all listings.
        """
        properties = []
        for listing in self.listings.values():
            properties.extend(listing.properties)
        return properties

    def get_flat_dict(self):
        """Returns a flat dictionary of all properties.
        
        Returns:
            list[dict]: A list of dictionaries representing each property.
        """
        from dataclasses import asdict
        return [asdict(prop) for prop in self.get_all_properties()]