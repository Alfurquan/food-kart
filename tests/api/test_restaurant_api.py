import pytest
from unittest.mock import MagicMock
from foodkart.api.restaurant_api import RestaurantAPI
from foodkart.models.restaurant import Restaurant
from foodkart.models.menuitem import MenuItem
from foodkart.exception import RestaurantNameMissingException,RestaurantNotFoundException, RestaurantCapacityLessThanZeroException, MenuNameMissingException, MenuPriceNegativeException

@pytest.fixture()
def restaurant_api(db):
    return RestaurantAPI(db)

@pytest.fixture()
def valid_restaurant():
    return Restaurant("Arsalan", 20)

@pytest.fixture()
def invalid_restaurant_name(request):
    return Restaurant(request.param, 20)

@pytest.fixture()
def invalid_restaurant_capacity():
    return Restaurant("Arsalan", -20)

@pytest.fixture()
def valid_menu_item():
    return MenuItem("Noodles", 100)

@pytest.fixture()
def invalid_menu_item_name(request):
    return MenuItem(request.param, 200)

@pytest.fixture()
def invalid_menu_item_price(request):
    return MenuItem("Noodles", -200)

def test_add_restuarant_valid_inputs(restaurant_api, db, valid_restaurant):
    db.create.return_value = 1
    
    id = restaurant_api.add_restaurant(valid_restaurant)
    
    assert id == 1
    db.create.assert_called_once_with(valid_restaurant.to_dict())
    db.update.assert_called_once_with(1, {'id': 1})    
    

@pytest.mark.parametrize('invalid_restaurant_name', ['', None, ' '], indirect=True)
def test_add_restaurant_name_invalid(restaurant_api, invalid_restaurant_name):
    with pytest.raises(RestaurantNameMissingException):
        restaurant_api.add_restaurant(invalid_restaurant_name)
        
def test_add_restaurant_capacity_negative(restaurant_api, invalid_restaurant_capacity):    
    with pytest.raises(RestaurantCapacityLessThanZeroException):
        restaurant_api.add_restaurant(invalid_restaurant_capacity)
     
def test_add_menu_item_restaurant_not_found(restaurant_api, db, valid_menu_item):
    db.get_item_by_id.return_value = None
    
    with pytest.raises(RestaurantNotFoundException):
        restaurant_api.add_menu_item(1, valid_menu_item)
    
        
def test_add_menu_item_empty_menu(restaurant_api, db, valid_menu_item, valid_restaurant):
     restaurant = valid_restaurant
     restaurant_api.get_restaurant = MagicMock(return_value = restaurant)
     
     menu_item_id = restaurant_api.add_menu_item(1, valid_menu_item)
     assert menu_item_id == 1
     assert len(restaurant.menu) == 1
     assert restaurant.menu[0].id == 1
     db.update.assert_called_once_with(1, restaurant.to_dict())
     
    
def test_add_menu_item_nonempty_menu(restaurant_api, db, valid_menu_item, valid_restaurant):
    restaurant = valid_restaurant
    existing_menu_item = MenuItem(name='Biryani', price=100)
    existing_menu_item.id = 1
    restaurant.menu.append(existing_menu_item)
    restaurant_api.get_restaurant = MagicMock(return_value = restaurant)
    
    menu_item_id = restaurant_api.add_menu_item(1, valid_menu_item)
    assert menu_item_id == 2
    assert len(restaurant.menu) == 2
    assert restaurant.menu[1].id == 2
    db.update.assert_called_once_with(1, restaurant.to_dict())
    
    


@pytest.mark.parametrize('invalid_menu_item_name', ['', None, ' '], indirect=True) 
def test_add_menu_item_invalid_menu_name(restaurant_api, invalid_menu_item_name):
    with pytest.raises(MenuNameMissingException):
        restaurant_api.add_menu_item(1, invalid_menu_item_name)
        
def test_add_menu_item_invalid_menu_price(restaurant_api, invalid_menu_item_price):
    with pytest.raises(MenuPriceNegativeException):
        restaurant_api.add_menu_item(1, invalid_menu_item_price)