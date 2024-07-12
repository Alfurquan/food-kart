import typer
from . import restaurant
from . import menu
from . import order
from . import customer


app = typer.Typer(no_args_is_help=True, help="Foodkart is a small food delivery CLI app")
app.add_typer(restaurant.app, name='restaurants')
app.add_typer(menu.app, name='menu')
app.add_typer(order.app, name='orders')
app.add_typer(customer.app, name='customers')

