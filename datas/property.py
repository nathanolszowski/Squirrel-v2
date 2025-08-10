# -*- coding: utf-8 -*-
"""
Property dataclass to represent a property with its details.
This module defines the Property dataclass which includes various attributes related to a property such as agency, Url,...
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class Property:
    """Represents a property with its details."""
    agency:Optional[str]
    url:Optional[str]
    reference:Optional[str]
    asset_type:Optional[str]
    contract:Optional[str]
    disponibility:Optional[str]
    area:Optional[str]
    division:Optional[str]
    adress:Optional[str]
    postal_code:Optional[str]
    contact:Optional[str]
    resume:Optional[str]
    amenities:Optional[str]
    url_image:Optional[str]
    latitude:Optional[float]
    longitude:Optional[float]
    price:Optional[str]