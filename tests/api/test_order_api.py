import pytest
from unittest.mock import Mock, patch, call
from foodkart.api.restaurant_api import RestaurantAPI
from foodkart.api.order_api import OrderAPI
from foodkart.api.customer_api import CustomerAPI
from foodkart.exception import CustomerNotFoundException, OrderNotFoundException, OrderAlreadyDelivered
from foodkart.models.customer import Customer
from foodkart.models.restaurant import Restaurant
from foodkart.models.menuitem import MenuItem
from foodkart.models.order import OrderStatus, Order, OrderItem

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
    expected_orders = [
        Order(id=1, customer_id=1, restaurant_id=2, 
              restaurant_name='Arsalan', cost=300, order_status='Delivered', 
              items=[OrderItem(name='Biryani', quantity=1), 
                     OrderItem(name='Noodles', quantity=1)]),
        Order(id=2, customer_id=2, restaurant_id=2, 
              restaurant_name='Arsalan', cost=300, order_status='Delivered', 
              items=[OrderItem(name='Biryani', quantity=1), 
                     OrderItem(name='Noodles', quantity=1)]),
        
    ] 
    
    db.get_all.return_value = orders
        
    actual_orders = order_api.list_orders()
    
    assert actual_orders == expected_orders
    
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
        Order(id=1, customer_id=1, restaurant_id=2, 
              restaurant_name='Arsalan', cost=300, order_status='Delivered', 
              items=[OrderItem(name='Biryani', quantity=1), 
                     OrderItem(name='Noodles', quantity=1)])    
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
        
        
def test_create_orders_multiple_items_from_diff_restaurant(order_api, customer_api, restaurant_api, db):    
    db.create.side_effect = lambda order: 1 if order['restaurant_id'] == 1 else 2 
    customer = Customer(1, 'John', '7003404263')
    restaurant_one = Restaurant(id=1, name='Arsalan', processing_capacity=20, menu=[MenuItem(id=1, name='Biryani', price=200)])
    restaurant_two = Restaurant(id=2, name='KFC', processing_capacity=15, menu=[MenuItem(id=1, name='Noodles', price=100)])
    
    customer_api.get_customer.return_value = customer
    restaurant_api.get_restaurant.side_effect = lambda order_id: restaurant_one if order_id == 1 else restaurant_two

    with patch('foodkart.strategy.api.StrategyAPI.get_restaurant_selection_strategy') as get_restaurant_selection_strategy_mock:
        restaurant_selection = Mock()
        restaurant_selection.select_restaurant = Mock(side_effect=lambda food_item: restaurant_one if food_item == ('Biryani', 1) else (restaurant_two if food_item == ('Noodles', 2) else None))
        get_restaurant_selection_strategy_mock.return_value = restaurant_selection
        
        result = order_api.create_orders(1, ['Biryani', 'Noodles'], [1, 2])

        assert len(result) == 2
        assert result[0].id == 1
        assert result[0].restaurant_id == 1
        assert result[0].cost == 200
        assert result[0].items[0].name == "Biryani"
        assert result[0].items[0].quantity == 1
        assert restaurant_one.processing_capacity == 19
        
        assert result[1].id == 2
        assert result[1].restaurant_id == 2
        assert result[1].cost == 200
        assert result[1].items[0].name == "Noodles"
        assert result[1].items[0].quantity == 2
        assert restaurant_two.processing_capacity == 13

        # Verifying DB interactions
        db.create.call_count == 2
        db.update.assert_has_calls([call(1, {'id':1}), call(2, {'id': 2})])
        db.close.assert_called_once()

        # # Verifying restaurant API interactions
        restaurant_api.get_restaurant.assert_has_calls([call(1), call(2)])
        restaurant_api.update_restaurant.assert_has_calls([call(1, restaurant_one), call(2, restaurant_two)])
        
def test_create_orders_multiple_items_from_same_restaurant(order_api, customer_api, restaurant_api, db):    
    db.create.side_effect = lambda order: 1 if order['restaurant_id'] == 1 else 2 
    customer = Customer(1, 'John', '7003404263')
    restaurant_one = Restaurant(id=1, name='Arsalan', processing_capacity=20, menu=[MenuItem(id=1, name='Biryani', price=200), MenuItem(id=2, name='Kebab', price = 100)])
    restaurant_two = Restaurant(id=2, name='KFC', processing_capacity=15, menu=[MenuItem(id=1, name='Noodles', price=100)])
    
    customer_api.get_customer.return_value = customer
    restaurant_api.get_restaurant.side_effect = lambda order_id: restaurant_one if order_id == 1 else restaurant_two

    with patch('foodkart.strategy.api.StrategyAPI.get_restaurant_selection_strategy') as get_restaurant_selection_strategy_mock:
        restaurant_selection = Mock()
        restaurant_selection.select_restaurant = Mock(side_effect=lambda food_item: restaurant_one if food_item == ('Biryani', 2) or food_item == ('Kebab', 2) else (restaurant_two if food_item == ('Noodles', 2) else None))
        get_restaurant_selection_strategy_mock.return_value = restaurant_selection
        
        result = order_api.create_orders(1, ['Biryani', 'Noodles', 'Kebab', 'Manchurian'], [2, 2, 2, 3])

        assert len(result) == 3
        assert result[0].id == 1
        assert result[0].restaurant_id == 1
        assert result[0].cost == 600
        assert result[0].items[0].name == "Biryani"
        assert result[0].items[0].quantity == 2
        assert result[0].items[1].name == "Kebab"
        assert result[0].items[1].quantity == 2
        assert result[0].order_status == OrderStatus.Processing.value
        assert restaurant_one.processing_capacity == 16
        
        assert result[1].id == 2
        assert result[1].restaurant_id == 2
        assert result[1].cost == 200
        assert result[1].items[0].name == "Noodles"
        assert result[1].items[0].quantity == 2
        assert result[1].order_status == OrderStatus.Processing.value
        assert restaurant_two.processing_capacity == 13
        
        
        assert result[2].id == None
        assert result[2].restaurant_id == None
        assert result[2].cost == 0
        assert result[2].items[0].name == "Manchurian"
        assert result[2].items[0].quantity == 3
        assert result[2].order_status == OrderStatus.CannotServe.value

        # Verifying DB interactions
        db.create.call_count == 2
        db.update.assert_has_calls([call(1, {'id':1}), call(2, {'id': 2})])
        db.close.assert_called_once()

        # # Verifying restaurant API interactions
        restaurant_api.get_restaurant.assert_has_calls([call(1), call(2)])
        restaurant_api.update_restaurant.assert_has_calls([call(1, restaurant_one), call(2, restaurant_two)])
        
def test_deliver_order_order_not_found(order_api, db):
    db.get_item_by_id.return_value = None
    
    with pytest.raises(OrderNotFoundException):
        order_api.deliver_order(1)
        
def test_deliver_order_order_already_delivered(order_api, db):
    db.get_item_by_id.return_value =  {
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
    
    with pytest.raises(OrderAlreadyDelivered):
        order_api.deliver_order(1)
        
def test_deliver_order_order_not_delivered(order_api, restaurant_api, db):
    order_document =  {
          'id':1,
          'customer_id':1,
          'restaurant_id': 2,
          'restaurant_name': 'Arsalan',
          'cost': 300,
          'order_status': 'Processing',
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
    db.get_item_by_id.return_value =  order_document
    order = Order.from_dict(order_document)
    restaurant = Restaurant(id=1, name='Arsalan', processing_capacity=20, menu=[MenuItem(id=1, name='Biryani', price=200)])
    restaurant_api.get_restaurant.return_value = restaurant
    
    actual_order = order_api.deliver_order(1)
    
    
    ## Verify model changes
    assert actual_order.order_status == OrderStatus.Delivered.value
    assert restaurant.processing_capacity == 22
    
    ## Verify db interactions
    db.get_item_by_id.assert_called_once_with(1)
    db.update.assert_called_once_with(1, actual_order.to_dict())
    restaurant_api.update_restaurant.assert_called_once_with(actual_order.restaurant_id, restaurant)