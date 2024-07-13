import pytest
from foodkart.api.restaurant_api import RestaurantAPI
from foodkart.models.restaurant import Restaurant

def test_add_restuarant_correct_inputs(foodkart_db):
    api = RestaurantAPI(foodkart_db)
    restaurant = Restaurant("Arsalan", 20)
    id = api.add_restaurant(restaurant)
    assert restaurant == api.get_restaurant(id)