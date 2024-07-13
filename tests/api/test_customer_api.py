import pytest
from foodkart.models.customer import Customer
from foodkart.api.customer_api import CustomerAPI
from foodkart.exception import CustomerNameMissing, CustomerPhoneMissing

def test_add_customer_valid_inputs(foodkart_db):
    api = CustomerAPI(foodkart_db)
    customer = Customer("John", "7003404263")
    id = api.add_customer(customer)
    assert customer == api.get_customer(id)

@pytest.mark.parametrize('customer_name', ['', None, ' '])
def test_add_customer_name_missing(foodkart_db, customer_name):
    api = CustomerAPI(foodkart_db)
    customer = Customer(customer_name, "7003404263")
    with pytest.raises(CustomerNameMissing):
        api.add_customer(customer)
        
@pytest.mark.parametrize('customer_phone', ['', None, ' '])
def test_add_customer_phone_missing(foodkart_db, customer_phone):
    api = CustomerAPI(foodkart_db)
    customer = Customer("John", customer_phone)
    with pytest.raises(CustomerPhoneMissing):
        api.add_customer(customer)
        
