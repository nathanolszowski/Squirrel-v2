# -*- coding: utf-8 -*-
"""
Property listing module
This module defines the PropertyListing class which represents a collection of properties with their details.
It includes methods to create properties and manage the listing.
"""
from datas.property import Property

class PropertyListing:
    """Represents a collection of properties with their details."""
    
    def __init__(self, name_agency_listing: str):
        """Initializes an empty property listing."""
        self.name_agency_listing = name_agency_listing
        self.properties:list[Property] = []
        self.failed_urls:list[str] | None = []
        
    def create_property(self, property:Property) -> Property:
        """Creates a new property and adds it to the listing.
        
        Returns:
            property (Property): The created property instance.
        """
        self.properties.append(property)
        return property
    
    def count_properties(self) -> int:
        """Returns the number of properties in the listing.
        
        Returns: 
            int: The number of proerties in the listing.
        """
        return len(self.properties)