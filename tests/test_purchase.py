from flask import Flask
from flask.testing import FlaskClient
from flask_mysqldb import MySQL

ENDPOINT = "/purchase"


def insert_sample_listing(client: FlaskClient):
    sample_param = {"product_id": "1", "vending_machine_id": "1", "quantity": "5"}

    listing_after_creating = client.post("/listing/create", query_string=sample_param)

    assert listing_after_creating.status_code == 200


def test_all_purchases(client: FlaskClient):
    get_all_purchases_response = client.get(ENDPOINT + "/all")
    assert get_all_purchases_response.status_code == 200


def test_purchases_by_vending_machine(client: FlaskClient, app_database: tuple[Flask, MySQL]):
    insert_sample_listing(client)
    sample_param = {"vending_machine_id": "1"}
    get_all_purchases_by_vending_machine_response = client.get(ENDPOINT + "/vending", query_string=sample_param)
    assert get_all_purchases_by_vending_machine_response.status_code == 200


def test_purchases_by_product(client: FlaskClient):
    sample_param = {"product_id": "1"}
    get_all_purchases_by_vending_machine_response = client.get(ENDPOINT + "/product", query_string=sample_param)
    assert get_all_purchases_by_vending_machine_response.status_code == 200
