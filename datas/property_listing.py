# -*- coding: utf-8 -*-
"""
Property listing module
"""
from datas.property import Property

class PropertyListing:
    """Represents a collection of properties with their details."""
    
    def __init__(self, name_agency_listing: str):
        """Initializes an empty property listing."""
        self.name_agency_listing = name_agency_listing
        self.properties:list[Property] = []
        
    def create_property(self, **kwargs) -> Property:
        """Creates a new property and adds it to the listing."""
        property = Property(**kwargs)
        self.properties.append(property)
        return property
    
    def count_properties(self) -> int:
        """Returns the number of properties in the listing."""
        return len(self.properties)