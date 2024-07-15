from .cheapest_price_restaurant_selection import CheapestPriceRestaurantSelection

class StrategyAPI:
    
    @classmethod
    def get_restaurant_selection_strategy(cls, restaurant_api):
        return CheapestPriceRestaurantSelection(restaurant_api)