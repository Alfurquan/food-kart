## Foodkart app

In Foodkart CLI app, we have three layers

- CLI: This is a thin layer which takes user input from command line and calls API layer
- API: This is the API layer where all the business logic resides.
- DB: This is thin layer which uses third party package tinydb to store data and retrieve data. 

Both cli and db layers are as thin as possible for a few reasons:
- Testing through the API tests most of the system and logic.
- Third-party dependencies are isolated to a single file.

For CLI layer we have these components
- customer cli layer: This manages CLI functions for customer operations like adding new customers
- restaurant cli layer: This manages CLI functions for retaurant operations.
- order cli layer: This manages CLI functions for order operations
- menu cli layer: This manages CLI functions for menu operations.

Similar to CLI layer, we have three API layers
- customer api
- restaurant api
- order api

The cli and db layer are thin, we will just write simple tests to make sure API is called correctly.
Most of the testing will be for the API layer which has all the logic.

### Evaluating features to test

Prioritize features to test based on the following factors:
- Recent—New features, new areas of code, new functionality that has been
recently repaired, refactored, or otherwise modified
- Core—Your product’s unique selling propositions (USPs). The essential
functions that must continue to work in order for the product to be useful
- Risk—Areas of the application that pose more risk, such as areas important to customers but not used regularly by the development team or
parts that use third-party code you don’t quite trust
- Problematic—Functionality that frequently breaks or often gets defect
reports against it
- Expertise—Features or algorithms understood by a limited subset of
people

For foodkart, here's how will go about

#### Core features

- customers
    - register customer
- restaurant
    - add restaurant, list restauarants
- menu
    - add menu to restaurant, update menu, list menu 
- order
    - create order, deliver order

### Generating test cases

- customer
    - register customer
        - correct inputs and customer is added to system
        - wrong name entered (e.g blank string), customer is not added
        - wrong phone enter, customer is not added
        - wrong name and phone entered, customer is not added

- restaurant 
    - add restaurant
        - correct inputs and restaurant is added to system
        - invalid name like empty string, restaurant is not added to system
        - invalid capacity like capacity < 0, restaurant is not added to system.
        - imvalid name and capacity, restauarnt is not added to system.

    - list restauarants
        - name provided, just list the specific restauarnt.
        - name not provided, list all restaurants.

- menu
    - add menu
        - correct inputs, menu is added to restaurant.
        - invalid name like empty string, menu is not added to restaurant.
        - invalid price, like price < 0, menu is not added to restaurant.
        - invalid rest id, rest does not exists, menu is not added.
        - all invalid inputs, menu is not added to restaurant.
    
    - update menu
        - correct inputs, menu is updated.
        - invalid menu item id, menu item does not exists
        - invalid menu item name, like blank string, menu item not updated
        - invalid price, menu item not updated
        - invalid rest id, rest does not exists, menu item not updated.

- order
    - create order
        - correct inputs, order is created.
        - invalid item name, order not created.
        - invalid quantity, order not created.
        - invalid cust id, cust does not exists, order not created
    
    - deliver order
        - correct input, order is marked delivered, rest process capacity reset.
        - invalid order id, order does not exists
        - order already delivered, do not deliver order again

- Restaurant selection strategy
    - test out rest selection strategy
        - rest with cheapest price for menu item
        - rest having same price for menu item, rest with more processing capacity selected
        - no rest found for the menu item, item cannot be served
