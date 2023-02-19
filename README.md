# Vending Machine Tracker API by: Karan Kumar 6380812

[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=karank85_vending-machine-tracker&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=karank85_vending-machine-tracker)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=karank85_vending-machine-tracker&metric=coverage)](https://sonarcloud.io/summary/new_code?id=karank85_vending-machine-tracker)

## Requirements for running

Run `poetry install` to make all the appropriate dependencies are downloaded

## Database setup

Make sure you have a mysql database connection ready. If needed change your credentials
in `cred.yaml` so that it will connect properly

To populate data `cd` to `tests/scripts` and run those sql scripts in your database so that tables and data will be populated

## API:

### Products

Components: product_id, name, price per unit

Get all products

```
GET 127.0.01:5000/product/all
```

Get a product's components based from id <br/>

```
GET 127.0.01:5000/product?id={id}
```

Delete a product

```
POST 127.0.0.1:5000/product/delete?id={id}
```

Create a product

```
POST 127.0.0.1:5000/product/create?name={name}&price={price}
```

Edit a product

```
POST 127.0.0.1:5000/product/edit?id={id}&name={name}&price={price}
```



### Listings

Components: vending_machine_id, product_id, quantity

Get all listings

```
GET 127.0.0.1:5000/listing/all
```

- Get a listing based on the machine and product it is

```
GET 127.0.0.1:5000/listing?product_id={product_id}&vending_machine_id={vending_machine_id}
```


- Purchase a listing (remove one stock from vending machine)

```
POST 127.0.0.1:5000/listing/buy?product_id={product_id}&vending_machine_id={vending_machine_id}
```

- Delete a listing

```
POST 127.0.0.1:5000/listing/delete?product_id={product_id}&vending_machine_id={vending_machine_id}
```

- Create a new listing

```
POST 127.0.0.1:5000/listing/create?product_id={product_id}&vending_machine_id={vending_machine_id}&quantity={quantity}
```

- Edit the listing

```
POST 127.0.0.1:5000/listing/edit?product_id={product_id}&vending_machine_id={vending_machine_id}&quantity={quantity}
```

### Vending Machine

Components: vending_machine_id, name, location

Get all vending machines

```
GET 127.0.0.1:500/vending-machine/all
```

- Get the vending machine information based on id

```
GET 127.0.0.1:5000/vending-machine?id={id}
```

- Delete vending machine

```
POST 127.0.0.1:5000/vending-machine/delete?id={id}
```

- Create a new vending machine

```
POST 127.0.0.1:5000/vending-machine/create?name={name}&location={location}
```

- Edit vending machine's information

```
POST 127.0.0.1:5000/vending-machine/edit?id={id}&name={name}&location={location}
```


### Extra Services

- Get all the products that is being sold in a certain vending machine

```
GET 127.0.0.1:5000/service/machine-stock?id={vending_machine_id}
```

- Get all the vending machines installed in a certain location

```
GET 127.0.0.1:5000/service/location-machine?location={location}
```

## How to run
run the following command in your terminal: `python3 app_run.py`

<b>Note:</b> Make sure you are in the right directory

## How to test

1. Connect to your localhost in MySQL data source
2. Create an empty schema with the name 'vending_tracker'

Recommended software: `Postman`

Send the correct request to each routes and with the correct parameters and values to get json output from each API

OR

Sample tests can be found in `tests/` to run those, use the command
```
pytest
```



#### Example:

![er_diagram](/static/postman.png)
