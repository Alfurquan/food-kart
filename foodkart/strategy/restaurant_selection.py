from abc import ABC, abstractmethod
from typing import List, Tuple
from ..models.order import OrderItem
from ..api.restaurant_api import RestaurantAPI

class RestaurantSelection(ABC):
    
    @abstractmethod
    def select_restaurant(self, food_item: Tuple[str, int]):
        """
        Selects restaurants for food item
        """
        raise NotImplementedError
    
    def get_eligible_restaurants(self, food_item: Tuple[str, int]):
        """
        Returns all restaurants that have food item specified and can process order
        """
        restaurants = self.restaurant_api.list_restaurants()
        food_item_name, food_item_quantity = food_item
        selected_restaurants = []
        for rest in restaurants:
            for menu_item in rest["menu"]:
                if menu_item["name"].lower() == food_item_name.lower() and rest["processing_capacity"] >= food_item_quantity:
                    selected_restaurants.append(rest)
        
        return selected_restaurants