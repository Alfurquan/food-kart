from ..data.db import DB
from ..models.customer import Customer
from ..config import config
from ..exception import CustomerNameMissing, CustomerPhoneMissing

class CustomerAPI:
    def __init__(self, db: DB = None):
        self.db_path = config.get_db_path()
        self.db = DB(self.db_path, "customer", "foodkart") if db is None else db
        
    def add_customer(self, customer: Customer):
        if not customer.name or customer.name == ' ':
            raise CustomerNameMissing
        
        if not customer.phone or customer.phone == ' ':
            raise CustomerPhoneMissing
        
        id = self.db.create(customer.to_dict())
        self.db.update(id, {"id": id})
        return id
    
    def get_customer(self, id: int):
        return Customer.from_dict(self.db.get_item_by_id(id))