import pytest
from foodkart.models.customer import Customer
from foodkart.api.customer_api import CustomerAPI
from foodkart.exception import CustomerNameMissingException, CustomerPhoneMissingException


@pytest.fixture()
def customer_api(db):
    return CustomerAPI(db)

@pytest.fixture
def valid_customer():
    return Customer(name="John Doe", phone="123456789")

@pytest.fixture
def invalid_customer_name(request):
    return Customer(name=request.param, phone="123456789")

@pytest.fixture
def invalid_customer_phone(request):
    return Customer(name="John Doe", phone=request.param)

def test_add_customer_valid_inputs(customer_api, valid_customer, db):
    db.create.return_value = 1
    customer_id = customer_api.add_customer(valid_customer)
    
    assert customer_id == 1
    db.create.assert_called_once_with(valid_customer.to_dict())
    db.update.assert_called_once_with(1, {'id': 1})


@pytest.mark.parametrize('invalid_customer_name', ['', None, ' '], indirect=True)
def test_add_customer_name_missing(customer_api, invalid_customer_name):
    with pytest.raises(CustomerNameMissingException):
        customer_api.add_customer(invalid_customer_name)
        
@pytest.mark.parametrize('invalid_customer_phone', ['', None, ' '], indirect=True)
def test_add_customer_phone_missing(customer_api, invalid_customer_phone):
    with pytest.raises(CustomerPhoneMissingException):
        customer_api.add_customer(invalid_customer_phone)
        
