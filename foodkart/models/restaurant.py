from dataclasses import dataclass, asdict, field
from typing import List
from .menuitem import MenuItem

@dataclass
class Restaurant:
    name: str = None
    processing_capacity: int = 0
    menu: List[MenuItem] = field(default_factory=list)
    id: int = field(default=None, compare=False)

    @classmethod
    def from_dict(cls, d):
        restaurant =  Restaurant(**d)
        menu = restaurant.menu
        restaurant.menu = []
        for menu_item in menu:
            restaurant.menu.append(MenuItem.from_dict(menu_item))
        
        return restaurant

    def to_dict(self):
        return asdict(self)