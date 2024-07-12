import typer
from typing import List
import rich
from rich.table import Table
from io import StringIO
from .api.restaurant_api import RestaurantAPI
from .models.menuitem import MenuItem
from .exception import RestaurantNotFoundException, MenuItemNotFoundException
from .utilities.validation import validate_price

app = typer.Typer(no_args_is_help=True)

@app.command()
def add(
    name: List[str] = typer.Argument(..., help="Name of menu item"),
    price: int = typer.Option(..., "--price", "-p", help="Price of menu item", callback=validate_price),
    restaurant_id : int = typer.Option(..., "--rest-id", help="Restaurant id for the menu")
):
    """
    Adds a menu item to menu of the restaurant id provided.
    """
    name = " ".join(name) if name else None
    api = RestaurantAPI()
    
    try:
        api.add_menu_item(restaurant_id, MenuItem(name, price))
        print("Menu item added to restaurant!")
    except RestaurantNotFoundException:
        print(f"Restaurant with id {restaurant_id} does not exist")
        
@app.command()
def list(
    rest_name: List[str] = typer.Argument(..., help="Name of restaurant")
):
    """
    Lists menu items for the restaurant provided
    """
    rest_name = " ".join(rest_name)
    api = RestaurantAPI()
    try:
        menu = api.get_menu_items(rest_name)
    except RestaurantNotFoundException:
        print(f"Restaurant with name {rest_name} not found!")
        raise typer.Exit(1)
    
    table = Table(box=rich.box.SIMPLE)
    table.add_column("name")
    table.add_column("Price")
    for item in menu:
        item = MenuItem.from_dict(item)
        table.add_row(item.name, str(item.price))
        
    out = StringIO()
    rich.print(table, file=out)
    print(out.getvalue())
    
@app.command()
def update(
    id : int = typer.Argument(..., help="Id of menu to be updated"),
    name: List[str] = typer.Argument(None, help="Name of menu item"),
    price: int = typer.Option(None, "--price", "-p", help="Price of menu item", callback=validate_price),
    restaurant_id : int = typer.Option(..., "--rest-id", help="Restaurant id for the menu")
):
    """
    updates a menu item to menu of the restaurant id provided.
    """
    name = " ".join(name) if name else None
    api = RestaurantAPI()
    
    try:
        api.update_menu_item(restaurant_id, MenuItem(name, price, id))
        print("Menu item updated for the restaurant!")
    except RestaurantNotFoundException:
        print(f"Restaurant with id {restaurant_id} does not exist")
    except MenuItemNotFoundException:
        print(f"Menu item with id {id} does not exists")