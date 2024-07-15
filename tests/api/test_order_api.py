import pytest
from unittest.mock import Mock
from foodkart.api.restaurant_api import RestaurantAPI
from foodkart.api.order_api import OrderAPI
from foodkart.api.customer_api import CustomerAPI

@pytest.fixture()
def restaurant_api():
    return Mock(spec=RestaurantAPI)

@pytest.fixture()
def customer_api():
    return Mock(spec=CustomerAPI)

@pytest.fixture()
def order_api(customer_api, restaurant_api, db):
    return OrderAPI(customer_api, restaurant_api, db)

def test_list_orders_customer_is_none(order_api, db):
    orders = [
        {
          'id':1,
          'customer_id':1,
          'restaurant_id': 2,
          'restaurant_name': 'Arsalan',
          'cost': 300,
          'order_status': 'Delivered',
          'items': [
              {
                  'name': 'Biryani',
                  'quantity': 1,
              },
              {
                  'name': 'Noodles',
                  'quantity': 1
              }
          ]  
        },
        {
          'id':2,
          'customer_id':2,
          'restaurant_id': 2,
          'restaurant_name': 'Arsalan',
          'cost': 300,
          'order_status': 'Delivered',
          'items': [
              {
                  'name': 'Biryani',
                  'quantity': 1,
              },
              {
                  'name': 'Noodles',
                  'quantity': 1
              }
          ]  
        }
    ]
    db.get_all.return_value = orders
        
    actual_orders = order_api.list_orders()
    
    assert actual_orders == orders
    
def test_list_orders_customer_is_not_none(order_api, db):
    orders = [
        {
          'id':1,
          'customer_id':1,
          'restaurant_id': 2,
          'restaurant_name': 'Arsalan',
          'cost': 300,
          'order_status': 'Delivered',
          'items': [
              {
                  'name': 'Biryani',
                  'quantity': 1,
              },
              {
                  'name': 'Noodles',
                  'quantity': 1
              }
          ]  
        },
        {
          'id':2,
          'customer_id':2,
          'restaurant_id': 2,
          'restaurant_name': 'Arsalan',
          'cost': 300,
          'order_status': 'Delivered',
          'items': [
              {
                  'name': 'Biryani',
                  'quantity': 1,
              },
              {
                  'name': 'Noodles',
                  'quantity': 1
              }
          ]  
        }
    ]
    expected_orders = [
         {
          'id':1,
          'customer_id':1,
          'restaurant_id': 2,
          'restaurant_name': 'Arsalan',
          'cost': 300,
          'order_status': 'Delivered',
          'items': [
              {
                  'name': 'Biryani',
                  'quantity': 1,
              },
              {
                  'name': 'Noodles',
                  'quantity': 1
              }
          ]  
        }
    ]
    db.get_all.return_value = orders
        
    actual_orders = order_api.list_orders(1)
    
    assert actual_orders == expected_orders
    