import pytest
from foodkart.api.restaurant_api import RestaurantAPI
from foodkart.models.restaurant import Restaurant
from foodkart.models.menuitem import MenuItem
from foodkart.exception import RestaurantNameMissingException, RestaurantCapacityLessThanZeroException, MenuNameMissingException, MenuPriceNegativeException

def test_add_restuarant_correct_inputs(foodkart_db):
    api = RestaurantAPI(foodkart_db)
    restaurant = Restaurant("Arsalan", 20)
    id = api.add_restaurant(restaurant)
    assert restaurant == api.get_restaurant(id)
    

@pytest.mark.parametrize('restaurant_name', ['', None, ' '])
def test_add_restaurant_name_invalid(foodkart_db, restaurant_name):
    api = RestaurantAPI(foodkart_db)
    restaurant = Restaurant(restaurant_name, 20)
    
    with pytest.raises(RestaurantNameMissingException):
        api.add_restaurant(restaurant)
        
def test_add_restaurant_capacity_negative(foodkart_db):
    api = RestaurantAPI(foodkart_db)
    restaurant = Restaurant("Arsalan", -20)
    
    with pytest.raises(RestaurantCapacityLessThanZeroException):
        api.add_restaurant(restaurant)
        
def test_add_menu_item_empty_menu(foodkart_db):
    api = RestaurantAPI(foodkart_db)
    id = api.add_restaurant(Restaurant("Arsalan", 20))
    id = api.add_menu_item(id, MenuItem("Biryani", 100))
    assert id == 1
    
def test_add_menu_item_nonempty_menu(foodkart_db):
    api = RestaurantAPI(foodkart_db)
    id = api.add_restaurant(Restaurant("Arsalan", 20, [MenuItem("Noodles", 100)]))
    restaurant = api.get_restaurant(id)
    menu_id = api.add_menu_item(id, MenuItem("Biryani", 100))
    assert menu_id == len(restaurant.menu) + 1

@pytest.mark.parametrize('menu_item_name', ['', None, ' ']) 
def test_add_menu_item_invalid_menu_name(foodkart_db, menu_item_name):
    api = RestaurantAPI(foodkart_db)
    menu_item = MenuItem(menu_item_name, 20)
    with pytest.raises(MenuNameMissingException):
        api.add_menu_item(1, menu_item)
        
def test_add_menu_item_invalid_menu_name(foodkart_db):
    api = RestaurantAPI(foodkart_db)
    menu_item = MenuItem('Noodles', -20)
    with pytest.raises(MenuPriceNegativeException):
        api.add_menu_item(1, menu_item)