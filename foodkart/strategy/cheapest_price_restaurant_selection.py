from typing import List, Tuple
from ..models.restaurant import Restaurant
from ..models.order import OrderItem
from .restaurant_selection import RestaurantSelection
from ..api.restaurant_api import RestaurantAPI

class CheapestPriceRestaurantSelection(RestaurantSelection):
    
    def select_restaurant(self, food_item: Tuple[str | int]):
        selected_restaurants = self.get_eligible_restaurants(food_item)
        food_item_name, food_item_quantity = food_item

        res = sorted(selected_restaurants, key=lambda x: (self.get_food_item_price(x, food_item_name), -x['processing_capacity']))
        selected_restaurant = res[0] if len(res) > 0 else None

        return selected_restaurant
        
        
    def get_food_item_price(self, restaurant, food_item):
        for item in restaurant['menu']:
            if item['name'].lower() == food_item.lower():
                return item['price']
        return int('inf')
