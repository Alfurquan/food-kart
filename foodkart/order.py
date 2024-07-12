import typer
import rich
from typing import List
from io import StringIO
from rich.table import Table
from .api.customer_api import CustomerAPI
from .api.order_api import OrderAPI
from .api.restaurant_api import RestaurantAPI
from .models.order import Order
from .exception import OrderNotFoundException, OrderAlreadyDelivered
from .utilities.validation import validate_quantity
app = typer.Typer(no_args_is_help=True)


@app.command()
def book(
    customer_id: int = typer.Option(..., "--customer-id", "-c", help="Customer id making the order"),
    item: List[str] = typer.Option(..., "--item", "-i", help="Name of item"),
    quantity: List[int] = typer.Option(..., "--quantity", "-q", help="Quantity of item", callback=validate_quantity),
):
    """
    Book an order for customer with id.
    """
    api = OrderAPI(CustomerAPI(), RestaurantAPI())
    
    if (len(item) != len(quantity)):
        print("Items and quantity do not match, please enter item and quantity in order. E.g --item <item name> --quantity <quantity of the item>")
        raise typer.Exit(1)

    orders: List[Order] =  api.create_orders(customer_id, item, quantity)
    servable_orders : List[Order] = [order for order in orders if order.restaurant_id is not None]
    not_servable_orders : List[Order] = [order for order in orders if order.restaurant_id is None]
    
    if len(servable_orders) == 0:
        print("Order cannot be placed as no restuarant found to server the items placed")
        raise typer.Exit(1)
    
    print("Order placed. Please check details....")
    table = Table(box=rich.box.SIMPLE)
    table.add_column("Id")
    table.add_column("Restaurant name")
    table.add_column("Order status")
    table.add_column("Cost")
    table.add_column("Order items")
    for order in servable_orders:
        table.add_row(str(order.id), order.restaurant_name, order.order_status, str(order.cost), str(order.items))
    
    out = StringIO()
    rich.print(table, file=out)
    print(out.getvalue())
    
    for order in not_servable_orders:
        for item in order.items:
            print(f"Item {item.name} cannot be served as no restaurant found to serve them")
            
@app.command()
def deliver(
    order_id: int = typer.Option(..., "--order-id", "-o", help="Order id to mark as delivered")
):
    """
    Mark the order by order id provided as delivered.
    """
    api = OrderAPI(CustomerAPI(), RestaurantAPI())
    
    try:
        api.deliver_order(order_id)
        print(f"Order {order_id} delivered to customer!")
    except OrderNotFoundException as ex:
        print(f"Order with id {order_id} not found!")
    except OrderAlreadyDelivered:
        print(f"Order with id {order_id} is already delivered!")
        

@app.command()
def list(
    customer_id: int = typer.Option(None, "--customer-id", "-c", help="Customer id to fetch orders for")
):
    """
    List all orders, and for a customer if customer id provided
    """
    api = OrderAPI(CustomerAPI(), RestaurantAPI())
    orders = api.list_orders(customer_id)
    table = Table(box=rich.box.SIMPLE)
    table.add_column("Id")
    table.add_column("Restaurant name")
    table.add_column("Order status")
    table.add_column("Cost")
    table.add_column("Order items")
    for order in orders:
        order = Order.from_dict(order)
        table.add_row(str(order.id), order.restaurant_name, order.order_status, str(order.cost), str(order.items))
    
    out = StringIO()
    rich.print(table, file=out)
    print(out.getvalue())