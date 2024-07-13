from ..data.db import DB
from ..models.customer import Customer
from ..exception import CustomerNameMissingException, CustomerPhoneMissingException, CustomerNotFoundException

class CustomerAPI:
    def __init__(self, db: DB):
        self.db = db
        self.db.set_table_name('customers')
        
    def add_customer(self, customer: Customer):
        if not customer.name or customer.name == ' ':
            raise CustomerNameMissingException
        
        if not customer.phone or customer.phone == ' ':
            raise CustomerPhoneMissingException
        
        id = self.db.create(customer.to_dict())
        self.db.update(id, {"id": id})
        return id
    
    def get_customer(self, id: int):
        customer = self.db.get_item_by_id(id)
        if customer is None:
            raise CustomerNotFoundException
        
        return Customer.from_dict(customer)