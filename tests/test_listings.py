from flask import Response
from flask.testing import FlaskClient

ENDPOINT = "/listing"


def listing_get_all(client: FlaskClient) -> Response:
    get_all_listing_response = client.get(ENDPOINT + "/all")

    assert get_all_listing_response.status_code == 200

    return get_all_listing_response.json


def test_listing_get_unique(client: FlaskClient):
    sample_param = {"product_id": "2", "vending_machine_id": "1"}
    get_a_single_listing = client.get(ENDPOINT, query_string=sample_param)

    assert get_a_single_listing.status_code == 200

    json_response_got = get_a_single_listing.json

    product_id_got = json_response_got["product_id"]
    vending_machine_got = json_response_got["vending_machine_id"]
    quantity_got = json_response_got["quantity"]

    assert product_id_got == 2 and vending_machine_got == 1 and quantity_got == 20


def test_listing_get_no_key_exist(client: FlaskClient):
    sample_fake_param = {"product_id": "9000", "vending_machine_id": "1"}
    get_a_single_listing = client.get(ENDPOINT, query_string=sample_fake_param)

    assert get_a_single_listing.status_code == 200

    json_response_got = get_a_single_listing.json

    response_status_got = json_response_got["success"]

    assert not response_status_got


def test_simple_purchase_listing(client: FlaskClient):
    def get_before_quantity_listing() -> int:
        sample_param_listing = {"product_id": "4", "vending_machine_id": "1"}
        get_a_single_listing = client.get(ENDPOINT, query_string=sample_param_listing)

        assert get_a_single_listing.status_code == 200

        before_json_response_got = get_a_single_listing.json

        quantity_before_got = before_json_response_got["quantity"]

        return quantity_before_got

    before_quantity = get_before_quantity_listing()

    sample_param = {"product_id": "4", "vending_machine_id": "1"}
    get_listing_after_buy = client.post(ENDPOINT + "/buy", query_string=sample_param)

    assert get_listing_after_buy.status_code == 200

    json_response_after_got = get_listing_after_buy.json

    quantity_after_got = json_response_after_got["quantity"]

    assert before_quantity - quantity_after_got == 1


def test_edit_listing(client: FlaskClient):
    pre_quantity_to_set = 90

    sample_param_pre_edit = {
        "product_id": "4",
        "vending_machine_id": "2",
        "quantity": str(pre_quantity_to_set),
    }

    get_listing_pre_edit = client.post(ENDPOINT + "/edit", query_string=sample_param_pre_edit)

    assert get_listing_pre_edit.status_code == 200

    json_response_pre_edit = get_listing_pre_edit.json

    quantity_pre_edit = json_response_pre_edit["quantity"]

    after_quantity_to_set = 95

    sample_param_after_edit = {
        "product_id": "4",
        "vending_machine_id": "2",
        "quantity": str(after_quantity_to_set),
    }

    get_listing_after_edit = client.post(ENDPOINT + "/edit", query_string=sample_param_after_edit)

    assert get_listing_after_edit.status_code == 200

    json_response_after_edit = get_listing_after_edit.json

    quantity_after_edit = json_response_after_edit["quantity"]

    assert quantity_after_edit != quantity_pre_edit


def test_delete_listing(client: FlaskClient):
    sample_param = {"product_id": "4", "vending_machine_id": "4"}

    get_listing_after_deleting = client.post(ENDPOINT + "/delete", query_string=sample_param)

    assert get_listing_after_deleting.status_code == 200


def test_create_listing(client: FlaskClient):

    before_create_json = listing_get_all(client)

    sample_param = {"product_id": "4", "vending_machine_id": "4", "quantity": "5"}
    get_listing_after_creating = client.post(ENDPOINT + "/create", query_string=sample_param)

    assert get_listing_after_creating.status_code == 200

    json_response_after_create = get_listing_after_creating.json

    assert before_create_json != json_response_after_create
