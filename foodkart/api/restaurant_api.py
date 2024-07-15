from ..data.db import DB
from ..models.restaurant import Restaurant, MenuItem
from typing import List
from ..exception import RestaurantNotFoundException, MenuItemNotFoundException, RestaurantNameMissingException, RestaurantCapacityLessThanZeroException, MenuNameMissingException, MenuPriceNegativeException

class RestaurantAPI:
    def __init__(self, db: DB):
        self.db = db
        self.db.set_table_name('restaurants')
   
    def add_restaurant(self, restaurant: Restaurant):
        if not restaurant.name or restaurant.name == ' ':
            raise RestaurantNameMissingException
        
        if restaurant.processing_capacity < 0:
            raise RestaurantCapacityLessThanZeroException
        
        id = self.db.create(restaurant.to_dict())
        self.db.update(id, {"id": id})
        return id
    
    def add_menu_item(self, rest_id: int, menu_item:MenuItem):
        if not menu_item.name or menu_item.name == ' ':
            raise MenuNameMissingException
        
        if menu_item.price < 0:
            raise MenuPriceNegativeException
        
        restaurant : Restaurant = self.get_restaurant(rest_id)
        
        menu = restaurant.menu
        
        if len(menu) == 0:
            menu_item.id = 1
        else:
            menu_item.id = len(menu) + 1
        
        restaurant.menu.append(menu_item)
        self.db.update(rest_id, restaurant.to_dict())
        return menu_item.id
    
    def update_menu_item(self, rest_id: int, menu_item: MenuItem):
        if not menu_item.name or menu_item.name == ' ':
            raise MenuNameMissingException
        
        if menu_item.price < 0:
            raise MenuPriceNegativeException
        
        restaurant : Restaurant = self.get_restaurant(rest_id)
        existing_menu_item = next((item for item in restaurant.menu if item.id == menu_item.id), None)
        
        if existing_menu_item is None:
            raise MenuItemNotFoundException
        
        print(menu_item)
        menu_items = restaurant.menu
        restaurant.menu = []
        for item in menu_items:
            if item.id == menu_item.id:
                if menu_item.name is not None:
                    item.name = menu_item.name
                
                if menu_item.price:
                    item.price = menu_item.price
            restaurant.menu.append(item)
        
        self.db.update(rest_id, restaurant.to_dict())
    
    def get_restaurant(self, id: int):
        restaurant = self.db.get_item_by_id(id)
        
        if restaurant is None:
            raise RestaurantNotFoundException
        
        return Restaurant.from_dict(restaurant)
    
    def update_restaurant(self, id: int, restaurant: Restaurant):
        self.db.update(id, restaurant.to_dict())
    
    def list_restaurants(self, name = None):
        restaurants = self.db.get_all()
        restaurant_list : List[Restaurant] = []
        
        if name is not None:
            restaurants = [restaurant for restaurant in restaurants if restaurant["name"].lower() == name.lower()]
        
        for restaurant in restaurants:
            rest = Restaurant.from_dict(restaurant)
            menu_items = rest.menu
            rest.menu = []
            for menu in menu_items:
                rest.menu.append(MenuItem.from_dict(menu))
            restaurant_list.append(rest)
        
        return restaurant_list
    
    def get_menu_items(self, rest_name):
        restaurants = self.list_restaurants(rest_name)
        
        restaurant = next((restaurant for restaurant in restaurants if restaurant.name.lower() == rest_name.lower()), None)
        
        if restaurant is None:
            raise RestaurantNotFoundException
        
        return restaurant.menu
        