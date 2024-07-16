import pytest
from unittest.mock import patch
from .utils import foodkart_cli

def test_register():
    with patch('foodkart.customer.CustomerAPI') as mock_cust_api:
        mock_cust_api.add_customer.return_value = 1
        output = foodkart_cli("customers register John --phone 7003404263")
        assert output == 'Customer with name John registered successfully!'