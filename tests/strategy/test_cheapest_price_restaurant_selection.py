import pytest
from unittest.mock import Mock, patch
from foodkart.api.restaurant_api import RestaurantAPI
from foodkart.models.restaurant import Restaurant
from foodkart.models.menuitem import MenuItem
from foodkart.strategy.cheapest_price_restaurant_selection import CheapestPriceRestaurantSelection

@pytest.fixture()
def restaurant_api():
    return Mock(spec=RestaurantAPI)

@pytest.fixture()
def cheapest_restaurant_selection(restaurant_api):
    return CheapestPriceRestaurantSelection(restaurant_api)


def test_get_food_item_price_food_item_not_found(cheapest_restaurant_selection):
    restaurant = Restaurant(id=1, name='Arsalan', processing_capacity=20, menu=[MenuItem(id=1, name='Biryani', price=200)])
    
    actual_price = cheapest_restaurant_selection.get_food_item_price(restaurant, 'Noodles')
    
    assert actual_price == float('inf')
    
def test_get_food_item_price_food_item_found(cheapest_restaurant_selection):
    restaurant = Restaurant(id=1, name='Arsalan', processing_capacity=20, menu=[MenuItem(id=1, name='Biryani', price=200)])
    
    actual_price = cheapest_restaurant_selection.get_food_item_price(restaurant, 'Biryani')
    
    assert actual_price == 200
    
def test_select_restaurant_no_restaurant_available(cheapest_restaurant_selection):
    food_item = ('Noodles', 5)
    with patch('foodkart.strategy.cheapest_price_restaurant_selection.CheapestPriceRestaurantSelection.get_eligible_restaurants') as eligible_rest_mock:
        eligible_rest_mock.side_effect = None

        actual_restaurant = cheapest_restaurant_selection.select_restaurant(food_item)
        
        assert actual_restaurant == None
        
def test_select_restaurant_restaurant_available_with_same_price(cheapest_restaurant_selection):
    food_item = ('Noodles', 5)
    restaurants = [
                   Restaurant(id=1, name='Arsalan', processing_capacity=4, menu=[MenuItem(id=1, name='Noodles', price=200)]), 
                   Restaurant(id=2, name='Mcdonalds', processing_capacity=2, menu=[MenuItem(id=1, name='Noodles', price=200)])
                ]
    with patch('foodkart.strategy.cheapest_price_restaurant_selection.CheapestPriceRestaurantSelection.get_eligible_restaurants') as eligible_rest_mock:
        eligible_rest_mock.return_value = restaurants

        actual_restaurant = cheapest_restaurant_selection.select_restaurant(food_item)
        
        assert actual_restaurant == restaurants[0]
        
def test_select_restaurant_restaurant_available_with_different_price(cheapest_restaurant_selection):
    food_item = ('Noodles', 5)
    restaurants = [
                   Restaurant(id=1, name='Arsalan', processing_capacity=4, menu=[MenuItem(id=1, name='Noodles', price=200)]), 
                   Restaurant(id=2, name='Mcdonalds', processing_capacity=2, menu=[MenuItem(id=1, name='Noodles', price=150)])
                ]
    with patch('foodkart.strategy.cheapest_price_restaurant_selection.CheapestPriceRestaurantSelection.get_eligible_restaurants') as eligible_rest_mock:
        eligible_rest_mock.return_value = restaurants

        actual_restaurant = cheapest_restaurant_selection.select_restaurant(food_item)
        
        assert actual_restaurant == restaurants[1]
        
def test_get_eligible_restaurants_no_restaurant_found(cheapest_restaurant_selection):
    food_item = ('Noodles', 5)
    restaurants = [
                   Restaurant(id=1, name='Arsalan', processing_capacity=4, menu=[MenuItem(id=1, name='Noodles', price=200)]), 
                   Restaurant(id=2, name='Mcdonalds', processing_capacity=2, menu=[MenuItem(id=1, name='Noodles', price=200)])
                ]
    cheapest_restaurant_selection.restaurant_api = Mock(spec=RestaurantAPI)
    cheapest_restaurant_selection.restaurant_api.list_restaurants.return_value = restaurants
    
    actual_restaurants = cheapest_restaurant_selection.get_eligible_restaurants(food_item)
    
    assert actual_restaurants == []
    
def test_get_eligible_restaurants_restaurant_found(cheapest_restaurant_selection):
    food_item = ('Noodles', 5)
    restaurants = [
                   Restaurant(id=1, name='Arsalan', processing_capacity=10, menu=[MenuItem(id=1, name='Noodles', price=200)]), 
                   Restaurant(id=2, name='Mcdonalds', processing_capacity=12, menu=[MenuItem(id=1, name='Noodles', price=200)]),
                   Restaurant(id=2, name='Zeeshan', processing_capacity=2, menu=[MenuItem(id=1, name='Biryani', price=200)]),
                ]
    cheapest_restaurant_selection.restaurant_api = Mock(spec=RestaurantAPI)
    cheapest_restaurant_selection.restaurant_api.list_restaurants.return_value = restaurants
    
    expected_restaurants = restaurants[0:2]
    
    actual_restaurants = cheapest_restaurant_selection.get_eligible_restaurants(food_item)
    
    assert actual_restaurants == expected_restaurants
    
