from flask.testing import FlaskClient

ENDPOINT = "/purchase"


def test_all_purchases(client: FlaskClient):
    get_all_purchases_response = client.get(ENDPOINT + "/all")
    assert get_all_purchases_response.status_code == 200


def test_purchases_by_vending_machine(client: FlaskClient):
    sample_param = {"id": "2"}
    get_all_purchases_by_vending_machine_response = client.get(ENDPOINT + "/vending", query_string=sample_param)
    assert get_all_purchases_by_vending_machine_response.status_code == 200


def test_purchases_by_product(client: FlaskClient):
    sample_param = {"id": "2"}
    get_all_purchases_by_vending_machine_response = client.get(ENDPOINT + "/product", query_string=sample_param)
    assert get_all_purchases_by_vending_machine_response.status_code == 200
