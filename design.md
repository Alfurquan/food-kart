### Model classes

- Restaurant
    ```python
    id: int
    name: str
    menu: list(MenuItem)
    processing_capability: int
    ```
- MenuItem
    ```python
    id: int
    name: str
    price: float
    ```

- Customer
    ```python
    id: int
    email: int
    phone: str
    username: str
    name: str
    ```

- Order
    ```python
    id: int
    customer_id: int
    restaurant_id: int
    items: list(MenuItem)
    cost: int
    order_status: OrderStatus
    ```
- OrderStatus (Enum)
    ```python
    PROCESSING
    DELIVERED
    ```
