# -*- coding: utf-8 -*-
"""
Testing module for property and listing manager
"""

import pytest
import json
import io
from datas.property import Property
from datas.property_listing import PropertyListing
from datas.listing_manager import ListingManager
from datas.listing_exporter import ListingExporter


@pytest.fixture
def property_fixture():
    return Property(
        agency="ImmoTest",
        url="https://test.com/annonce/1",
        reference="REF123",
        asset_type="office",
        contract="Vente",
        disponibility="Immédiate",
        area="100 m²",
        division="Non divisible",
        adress="1 rue du test",
        postal_code="75000",
        contact="Agence Test",
        resume="Superbe bien",
        amenities="Rénové",
        url_image="https://test.com/img.jpg",
        latitude=48.85,
        longitude=2.35,
        price="500000"
    )
    
class TestPropertyClasses:
    """Regroup all tests related to property and listing classes."""
    
    def test_property_creation(self, property_fixture):
        prop = property_fixture
        assert prop.agency == "ImmoTest"
        assert prop.area == "100 m²"
        assert prop.latitude == 48.85
        assert prop.price == "500000"

    def test_propertylisting_add_and_count(self, property_fixture):
        listing = PropertyListing("ImmoTest")
        assert listing.count_properties() == 0
        listing.properties.append(property_fixture)
        assert listing.count_properties() == 1

    def test_listingmanager_add_and_flat(self, property_fixture):
        manager = ListingManager()
        listing = PropertyListing("ImmoTest")
        listing.properties.append(property_fixture)
        manager.listings["ImmoTest"] = listing

        all_props = manager.get_all_properties()
        assert len(all_props) == 1
        assert all_props[0].reference == "REF123"

        flat = manager.get_flat_dict()
        assert isinstance(flat, list)
        assert isinstance(flat[0], dict)
        assert flat[0]["agency"] == "ImmoTest"
"""
    def test_listingexporter_to_json(self, property_fixture, monkeypatch):
        listing = PropertyListing("ImmoTest")
        listing.properties.append(property_fixture)
        exporter = ListingExporter(listing)

        fake_file = io.StringIO()
        exporter.export_to_json("fakepath.json", fileobj=fake_file)
        fake_file.seek(0)
        data = json.load(fake_file)
        assert data[0]["reference"] == "REF123"
"""