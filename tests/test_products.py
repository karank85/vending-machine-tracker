from flask import Response
from flask.testing import FlaskClient

ENDPOINT = "/product"


def product_get_all(client: FlaskClient) -> Response:
    get_all_product_response = client.get(ENDPOINT + "/all")

    assert get_all_product_response.status_code == 200

    return get_all_product_response.json


def test_product_get_unique(client: FlaskClient):
    sample_param = {"id": "2"}
    get_a_single_product = client.get(ENDPOINT, query_string=sample_param)

    assert get_a_single_product.status_code == 200

    json_response_got = get_a_single_product.json

    product_id_got = json_response_got["product_id"]
    product_name_got = json_response_got["product_name"]
    price_got = json_response_got["price"]

    assert product_id_got == 2 and product_name_got == "coke" and price_got == 25


def test_product_get_no_key_exist(client: FlaskClient):
    sample_fake_param = {"id": "9000"}

    get_a_single_product = client.get(ENDPOINT, query_string=sample_fake_param)

    assert get_a_single_product.status_code == 200

    json_response_got = get_a_single_product.json

    response_status_got = json_response_got["success"]

    assert not response_status_got


def test_edit_product(client: FlaskClient):

    sample_param_pre_edit = {"id": "5", "name": "yoyo", "price": "80"}

    get_product_pre_edit = client.post(ENDPOINT + "/edit", query_string=sample_param_pre_edit)

    assert get_product_pre_edit.status_code == 200

    json_response_pre_edit = get_product_pre_edit.json

    price_pre_edit = json_response_pre_edit["price"]
    name_pre_edit = json_response_pre_edit["product_name"]

    sample_param_after_edit = {"id": "5", "name": "snickers", "price": "314"}

    get_product_after_edit = client.post(ENDPOINT + "/edit", query_string=sample_param_after_edit)

    assert get_product_after_edit.status_code == 200

    json_response_after_edit = get_product_after_edit.json

    price_after_edit = json_response_after_edit["price"]
    name_after_edit = json_response_after_edit["product_name"]

    assert name_after_edit != name_pre_edit and price_pre_edit != price_after_edit


def test_create_listing(client: FlaskClient):

    before_create_json = product_get_all(client)

    sample_param = {"name": "cheetos", "price": "80"}
    get_product_after_creating = client.post(ENDPOINT + "/create", query_string=sample_param)

    assert get_product_after_creating.status_code == 200

    json_response_after_create = get_product_after_creating.json

    assert before_create_json != json_response_after_create


def test_delete_product(client: FlaskClient):

    sample_param = {"id": "6"}

    get_listing_after_deleting = client.post(ENDPOINT + "/delete", query_string=sample_param)

    assert get_listing_after_deleting.status_code == 200
