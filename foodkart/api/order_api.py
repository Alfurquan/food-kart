from typing import List
from ..config import config
from ..data.db import DB
from .customer_api import CustomerAPI
from .restaurant_api import RestaurantAPI
from ..exception import CustomerNotFoundException, OrderNotFoundException, OrderAlreadyDelivered
from ..strategy import get_restaurant_selection_strategy
from ..strategy.restaurant_selection import RestaurantSelection
from ..models.order import Order, OrderItem, OrderStatus
from ..models.restaurant import Restaurant

class OrderAPI:
    def __init__(self, customer_api : CustomerAPI, restaurant_api: RestaurantAPI, db: DB):
        self.db = db
        self.customer_api = customer_api
        self.restaurant_api = restaurant_api
        self.db.set_table_name('orders')
    
    def list_orders(self, cust_id: int = None):
        orders = self.db.get_all()
        
        if cust_id is not None:
            orders = [
                    order 
                    for order in orders
                    if order['customer_id'] == cust_id
            ]
        
        self.db.close()
        return orders
    
    def create_orders(self, cust_id: int, items: List[str], quantities: List[int]):
        customer = self.customer_api.get_customer(cust_id)
        
        if customer is None:
            raise CustomerNotFoundException
        
        food_items = list(zip(items, quantities))
        orders : List[Order] = []
        restaurant_selection : RestaurantSelection = get_restaurant_selection_strategy(self.restaurant_api)
        
        for food_item in food_items:
            food_item_name, food_item_quantity = food_item
            selected_restaurant = restaurant_selection.select_restaurant(food_item)
            order = Order(customer_id=cust_id)
            order_items : List[OrderItem] = []
            order_item = OrderItem(food_item_name, food_item_quantity)
            order_items.append(order_item)
            order.items = order_items
            cost = 0
            
            if not selected_restaurant:
                orders.append(order)
                continue
            
            cost = sum([menu['price'] for menu in selected_restaurant['menu'] if menu['name'].lower() == food_item_name.lower()]) * food_item_quantity
            
            orig_order = next((order for order in orders if order.restaurant_id == selected_restaurant['id']), None)
            
            if orig_order is not None:
                ## Update order for restaurant to include off this item         
                orig_order.cost += cost
                orig_order.items.append(order_item)
            else:
                ## Create off a new order 
                order.restaurant_id = selected_restaurant['id']
                order.restaurant_name = selected_restaurant['name']
                order.order_status = OrderStatus.Processing.value
                order.cost = cost
                orders.append(order)
            
        ## Save off order
        for order in orders:
            if order.restaurant_id is None:
                continue
            
            id = self.db.create(order.to_dict())
            self.db.update(id, {"id": id})
            order.id = id
        self.db.close()
        
        ## Update off restaurant processing capacity once order is made
        for order in orders:
            if order.restaurant_id is None:
                continue
            
            total_quantity = sum([item.quantity for item in order.items])
            restaurant = self.restaurant_api.get_restaurant(order.restaurant_id)
            capacity = restaurant.processing_capacity - total_quantity
            restaurant.processing_capacity = capacity
            self.restaurant_api.update_restaurant(order.restaurant_id, restaurant)   

        return orders
    
    def deliver_order(self, order_id: int):
        order: Order = Order.from_dict(self.db.get_item_by_id(order_id))
        
        if order is None:
            raise OrderNotFoundException
        
        if order.order_status == OrderStatus.Delivered.value:
            raise OrderAlreadyDelivered       
        # Set status as delivered
        order.order_status = OrderStatus.Delivered.value
        self.db.update(order_id, order.to_dict())
        self.db.close()
        
        # Add back restaurant processing capability
        restaurant : Restaurant = self.restaurant_api.get_restaurant(order.restaurant_id)
        quantities = sum([order_item["quantity"] for order_item in order.items])
        restaurant.processing_capacity += quantities
        self.restaurant_api.update_restaurant(order.restaurant_id, restaurant)
        