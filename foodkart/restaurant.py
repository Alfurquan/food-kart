import typer
import rich
from rich.table import Table
from io import StringIO
from typing import List
from .api.restaurant_api import RestaurantAPI
from .models.restaurant import Restaurant
from .utilities.validation import validate_capacity
from .config.config import get_db

app = typer.Typer(no_args_is_help=True)

@app.command()
def add(
    name: List[str] = typer.Argument(..., help="Enter name of restaurant"),
    capacity: int = typer.Option(..., "--capacity", "-c", help="Enter capacity of restaurant", callback=validate_capacity)
    ):
    """
    Adds a restaurant.
    """
    api = RestaurantAPI(get_db())
    name = " ".join(name) if name else None
    api.add_restaurant(Restaurant(name, capacity))
    print("Restaurant added!")
    
@app.command()
def list(
    name: List[str] = typer.Option(None, help="Enter name of restaurant in qoutes"),
    ):
    """
    List restaurants in the food kart chain
    """
    api = RestaurantAPI(get_db())
    name = " ".join(name) if name else None
    restaurants = api.list_restaurants(name)
    table = Table(box=rich.box.SIMPLE)
    table.add_column("Id")
    table.add_column("name")
    table.add_column("Processing capacity")
    table.add_column("Menu items")
    for restaurant in restaurants:
        restaurant = Restaurant.from_dict(restaurant)
        table.add_row(str(restaurant.id), restaurant.name, str(restaurant.processing_capacity), str(restaurant.menu))
    
    out = StringIO()
    rich.print(table, file=out)
    print(out.getvalue())