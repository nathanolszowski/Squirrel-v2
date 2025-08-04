# -*- coding: utf-8 -*-
"""
Property dataclass
"""

from dataclasses import dataclass

@dataclass
class Property:
    """Represents a property with its details."""
    agency:str
    url:str
    reference:str
    contract:str
    active:str
    disponibility:str
    area:str
    division:str
    adress:str
    postal_code:str
    contact:str
    resume:str
    aminties:str
    url_image:str
    latitude:float
    longitude:float
    price:float