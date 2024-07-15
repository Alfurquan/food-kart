import pytest
from unittest.mock import Mock, patch
from foodkart.api.restaurant_api import RestaurantAPI
from foodkart.api.order_api import OrderAPI
from foodkart.api.customer_api import CustomerAPI
from foodkart.exception import CustomerNotFoundException
from foodkart.models.customer import Customer
from foodkart.models.restaurant import Restaurant
from foodkart.models.menuitem import MenuItem

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
    
def test_create_orders_customer_not_found(order_api, customer_api):
    customer_api.get_customer.return_value = None
    
    with pytest.raises(CustomerNotFoundException):
        order_api.create_orders(1, ['Biryani'], [1])

def test_create_orders_single_item(order_api, customer_api, restaurant_api, db):
    db.create.return_value = 1
    customer = Customer(1, 'John', '7003404263')
    restaurant = Restaurant(id=1, name='Arsalan', processing_capacity=20, menu=[MenuItem(id=1, name='Biryani', price=200)])
    customer_api.get_customer.return_value = customer
    restaurant_api.get_restaurant.return_value = restaurant

    with patch('foodkart.strategy.api.StrategyAPI.get_restaurant_selection_strategy') as get_restaurant_selection_strategy_mock:
        restaurant_selection = Mock()
        restaurant_selection.select_restaurant = Mock(return_value = restaurant)
        get_restaurant_selection_strategy_mock.return_value = restaurant_selection
        

        result = order_api.create_orders(1, ["Biryani"], [1])

        assert len(result) == 1
        assert result[0].restaurant_id == 1
        assert result[0].cost == 200
        assert result[0].items[0].name == "Biryani"
        assert result[0].items[0].quantity == 1

        # Verifying DB interactions
        db.create.assert_called_once()
        db.update.assert_called_once_with(1, {"id": 1})
        db.close.assert_called_once()

        # Verifying restaurant API interactions
        restaurant_api.get_restaurant.assert_called_once_with(1)
        restaurant_api.update_restaurant.assert_called_once()