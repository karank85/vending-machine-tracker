import random

import requests
from flask import Response

ENDPOINT = "http://127.0.0.1:5000/"


def product_get_all() -> Response:
    get_all_product_response = requests.get(ENDPOINT + "/product/all")

    assert get_all_product_response.status_code == 200

    return get_all_product_response.json()


def test_product_get_unique():
    sample_param = {"id": "2"}
    get_a_single_product = requests.get(ENDPOINT + "product", params=sample_param)

    assert get_a_single_product.status_code == 200

    json_response_got = get_a_single_product.json()

    product_id_got = json_response_got["product_id"]
    product_name_got = json_response_got["product_name"]
    price_got = json_response_got["price"]

    assert product_id_got == 2 and product_name_got == "coke" and price_got == 25


def test_product_get_no_key_exist():
    sample_fake_param = {"id": "9000"}

    get_a_single_product = requests.get(ENDPOINT + "product", params=sample_fake_param)

    assert get_a_single_product.status_code == 200

    json_response_got = get_a_single_product.json()

    response_status_got = json_response_got["success"]

    assert not response_status_got


def test_edit_product():
    random_price_to_set = random.randint(10, 100)
    random_name_to_set = [
        "apple",
        "juice",
        "yoyo",
        "dsada",
        "dasdsa",
        "dasdasvf",
        "dasdasdasd",
        "asdasdasdas",
        "iiioe",
    ][random.randint(0, 8)]

    sample_param = {"id": "5", "name": random_name_to_set, "price": random_price_to_set}

    get_product_after_edit = requests.post(ENDPOINT + "/product/edit", params=sample_param)

    assert get_product_after_edit.status_code == 200

    json_response_after_edit = get_product_after_edit.json()

    price_after_edit = json_response_after_edit["price"]
    name_after_edit = json_response_after_edit["product_name"]

    assert name_after_edit == random_name_to_set and random_price_to_set == price_after_edit


def test_create_listing():
    sample_param = {"name": "cheetos", "price": "80"}
    get_product_after_creating = requests.post(ENDPOINT + "/product/create", params=sample_param)

    assert get_product_after_creating.status_code == 200

    json_response_after_create = get_product_after_creating.json()

    assert product_get_all() == json_response_after_create


def test_delete_product():
    sample_param = {"id": "6"}

    get_listing_after_deleting = requests.post(ENDPOINT + "/product/delete", params=sample_param)

    assert get_listing_after_deleting.status_code == 200

    json_response_after_delete = get_listing_after_deleting.json()

    assert product_get_all() == json_response_after_delete
