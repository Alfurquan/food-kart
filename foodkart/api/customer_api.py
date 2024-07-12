from ..data.db import DB
from ..models.customer import Customer
from ..config import config

class CustomerAPI:
    def __init__(self):
        self.db_path = config.get_db_path()
        self.db = DB(self.db_path, "customer", "foodkart")
        
    def add_customer(self, customer: Customer):
        id = self.db.create(customer.to_dict())
        self.db.update(id, {"id": id})
        self.db.close()
        return id
    
    def get_customer(self, id: int):
        return self.db.get_item_by_id(id)