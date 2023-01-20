# Vending Machine Tracker API by: Karan Kumar 6380812

## Features implemented:

### Products
Components: product_id (unique), name, price per unit
- Get all products 
- Get a product's components based from id
- Delete a product
- Create a product
- Edit the product components e.g coke, 20 -> cocacola, 25


### Listings 
Components: vending_machine_id, product_id, quantity
- Get all listings
- Get a listing based on the machine and product it is
- Purchase a listing (remove one stock from vending machine)
- Delete a listing
- Create a new listing 
- Edit the listing

### Vending Machine
Components: vending_machine_id, name, location
- Get all vending machines
- Get the vending machine information based on id
- Delete vending machine
- Create a new vending machine
- Edit vending machine's information


### Extra Services 
- Get all the products that is being sold in a certain vending machine
- Get all the vending machines installed in a certain location

### How to run
`cd` into the `app` directory then run the follow command in your terminal: `python3 __init__.py`

### How to test

Recommended software: `Postman`

Send the correct request to each routes and with the correct parameters and values to get json output from each API

#### Example:

![er_diagram](/static/postman.png)