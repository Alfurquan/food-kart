import typer
from typing import List
from .api.customer_api import CustomerAPI
from .models.customer import Customer
from .config.config import get_db

app = typer.Typer(no_args_is_help=True)

@app.command()
def register(
    name: List[str] = typer.Argument(..., help="Name of the customer"),
    phone: str = typer.Option(None, "--phone", "-p", help="Phone of the customer")
):
    """
    Register a customer to the app.
    """
    name = " ".join(name)
    api = CustomerAPI(get_db())
    id = api.add_customer(Customer(name, phone))
    print(f"Customer with name {name} registered successfully!")
    
