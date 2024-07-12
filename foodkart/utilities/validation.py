import typer
from typing import List

def validate_price(price : int):
    if price <= 0:
        raise typer.BadParameter("Price should be greated than equal to zero")
    return price
    
def validate_capacity(capacity: int):
    if capacity <= 0:
        raise typer.BadParameter("Capacity should be greated than equal to zero")
    return capacity

def validate_quantity(quantities : List[int]):
    for quantity in quantities:
        if quantity <= 0:
            raise typer.BadParameter("Quantity should be greated than equal to zero")
    return quantities