import random

from flask import Response
from flask.testing import FlaskClient


def listing_get_all(client: FlaskClient) -> Response:
    get_all_listing_response = client.get("/listing/all")

    assert get_all_listing_response.status_code == 200

    return get_all_listing_response.json


def test_listing_get_unique(client: FlaskClient):
    sample_param = {"product_id": "2", "vending_machine_id": "1"}
    get_a_single_listing = client.get("/listing", query_string=sample_param)

    assert get_a_single_listing.status_code == 200

    json_response_got = get_a_single_listing.json

    product_id_got = json_response_got["product_id"]
    vending_machine_got = json_response_got["vending_machine_id"]
    quantity_got = json_response_got["quantity"]

    assert product_id_got == 2 and vending_machine_got == 1 and quantity_got == 20


def test_listing_get_no_key_exist(client: FlaskClient):
    sample_fake_param = {"product_id": "9000", "vending_machine_id": "1"}
    get_a_single_listing = client.get("/listing", query_string=sample_fake_param)

    assert get_a_single_listing.status_code == 200

    json_response_got = get_a_single_listing.json

    response_status_got = json_response_got["success"]

    assert not response_status_got


def test_simple_purchase_listing(client: FlaskClient):
    def get_before_quantity_listing() -> int:
        sample_param_listing = {"product_id": "4", "vending_machine_id": "1"}
        get_a_single_listing = client.get("/listing", query_string=sample_param_listing)

        assert get_a_single_listing.status_code == 200

        before_json_response_got = get_a_single_listing.json

        quantity_before_got = before_json_response_got["quantity"]

        return quantity_before_got

    before_quantity = get_before_quantity_listing()

    sample_param = {"product_id": "4", "vending_machine_id": "1"}
    get_listing_after_buy = client.post("/listing/buy", query_string=sample_param)

    assert get_listing_after_buy.status_code == 200

    json_response_after_got = get_listing_after_buy.json

    quantity_after_got = json_response_after_got["quantity"]

    assert before_quantity - quantity_after_got == 1


def test_edit_listing(client: FlaskClient):
    random_quantity_to_set = random.randint(10, 100)

    sample_param = {
        "product_id": "4",
        "vending_machine_id": "2",
        "quantity": str(random_quantity_to_set),
    }

    get_listing_after_edit = client.post("/listing/edit", query_string=sample_param)

    assert get_listing_after_edit.status_code == 200

    json_response_after_edit = get_listing_after_edit.json

    quantity_after_edit = json_response_after_edit["quantity"]

    assert quantity_after_edit == random_quantity_to_set


def test_delete_listing(client: FlaskClient):
    sample_param = {"product_id": "4", "vending_machine_id": "4"}

    get_listing_after_deleting = client.post("/listing/delete", query_string=sample_param)

    assert get_listing_after_deleting.status_code == 200

    json_response_after_delete = get_listing_after_deleting.json

    assert listing_get_all(client) == json_response_after_delete


def test_create_listing(client: FlaskClient):
    sample_param = {"product_id": "4", "vending_machine_id": "4", "quantity": "5"}
    get_listing_after_creating = client.post("/listing/create", query_string=sample_param)

    assert get_listing_after_creating.status_code == 200

    json_response_after_create = get_listing_after_creating.json

    assert listing_get_all(client) == json_response_after_create
