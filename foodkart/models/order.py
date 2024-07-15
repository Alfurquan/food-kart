from dataclasses import dataclass, asdict, field
from typing import List
from enum import Enum
from .menuitem import MenuItem

class OrderStatus(Enum):
    CannotServe = 'CannotServe'
    Processing = 'Processing'
    Delivered = 'Delivered'


@dataclass
class OrderItem:
    name: str
    quantity: int
    
    @classmethod
    def from_dict(cls, d):
        return OrderItem(**d)
    
    def __repr__(self):
        return f"{self.name}: {self.quantity}"
    
    def to_dict(self):
        return asdict(self)
    
    def __hash__(self):
        return hash((self.name, self.quantity))


@dataclass
class Order:
    customer_id: int   
    restaurant_id: int = None
    restaurant_name: str = None
    items: List[OrderItem] = field(default_factory=list)
    order_status : OrderStatus = OrderStatus.CannotServe.value
    cost : int = 0
    id: int = field(default=None, compare=False)

    @classmethod
    def from_dict(cls, d):
        order = Order(**d)
        items = order.items
        order.items = []
        for item in items:
            order.items.append(OrderItem.from_dict(item))
        
        return order
    
    def to_dict(self):
        return asdict(self)
    

    
    