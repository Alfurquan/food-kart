from ..data.db import DB
from ..models.restaurant import Restaurant, MenuItem
from ..config import config
from ..exception import RestaurantNotFoundException, MenuItemNotFoundException

class RestaurantAPI:
    def __init__(self, db: DB):
        self.db = db
        self.db.set_table_name('restaurants')
   
    def add_restaurant(self, restaurant: Restaurant):
        id = self.db.create(restaurant.to_dict())
        self.db.update(id, {"id": id})
        return id
    
    def add_menu_item(self, rest_id: int, menu_item:MenuItem):
        restaurant : Restaurant = self.db.get_item_by_id(rest_id)
        
        if restaurant is None:
            raise RestaurantNotFoundException
        
        restaurant = Restaurant.from_dict(restaurant)
        menu = restaurant.menu
        
        if len(menu) == 0:
            menu_item.id = 1
        else:
            menu_item.id = len(menu) + 1
        
        restaurant.menu.append(menu_item)
        self.db.update(rest_id, restaurant.to_dict())
        self.db.close()
        return menu_item.id
    
    def update_menu_item(self, rest_id: int, menu_item: MenuItem):
        restaurant : Restaurant = self.db.get_item_by_id(rest_id)
        
        if restaurant is None:
            raise RestaurantNotFoundException
        
        restaurant = Restaurant.from_dict(restaurant)
        
        existing_menu_item = next((item for item in restaurant.menu if item['id'] == menu_item.id), None)

        if existing_menu_item is None:
            raise MenuItemNotFoundException
        
        restaurant.menu = [
            {**item, 'name': menu_item.name} if item['id'] == menu_item.id and menu_item.name is not None else item for item in restaurant.menu
        ]
        
        restaurant.menu = [
            {**item, 'price': menu_item.price} if item['id'] == menu_item.id and menu_item.price is not None else item for item in restaurant.menu
        ]
        
        self.db.update(rest_id, restaurant.to_dict())
        self.db.close()
    
    def get_restaurant(self, id: int):
        return Restaurant.from_dict(self.db.get_item_by_id(id))
    
    def update_restaurant(self, id: int, restaurant: Restaurant):
        self.db.update(id, restaurant.to_dict())
    
    def list_restaurants(self, name = None):
        restaurants = self.db.get_all()
        
        if name is not None:
            restaurants = [restaurant for restaurant in restaurants if restaurant["name"].lower() == name.lower()]
            
        return restaurants
    
    def get_menu_items(self, rest_name):
        restaurants = self.db.get_all()
        self.db.close()
        
        restaurant = next((restaurant for restaurant in restaurants if restaurant['name'].lower() == rest_name.lower()), None)
        
        if restaurant is None:
            raise RestaurantNotFoundException
        
        return restaurant['menu']
        