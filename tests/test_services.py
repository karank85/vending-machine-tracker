from flask.testing import FlaskClient

ENDPOINT = "/service"


def test_service_vending_machine_stock(client: FlaskClient):
    sample_param = {"id": "2"}
    get_all_vending_machine_stock_response = client.get(ENDPOINT + "/machine-stock", query_string=sample_param)

    assert get_all_vending_machine_stock_response.status_code == 200


def test_service_vending_machine_stock_wrong_arg(client: FlaskClient):
    sample_param = {"gimme_stock": "2"}
    get_all_vending_machine_stock_response = client.get(ENDPOINT + "/machine-stock", query_string=sample_param)

    assert get_all_vending_machine_stock_response.status_code == 200

    json_response_got = get_all_vending_machine_stock_response.json

    json_success_response = json_response_got["success"]

    assert not json_success_response


def test_service_vending_machine_location(client: FlaskClient):
    sample_param = {"location": "mlc"}
    get_all_vending_machine_at_location_response = client.get(ENDPOINT + "/location-machine", query_string=sample_param)

    assert get_all_vending_machine_at_location_response.status_code == 200

    get_single_vending_machine_at_location_json = get_all_vending_machine_at_location_response.json[0]

    vending_machine_id_got = get_single_vending_machine_at_location_json["vending_machine_id"]
    vending_machine_name_got = get_single_vending_machine_at_location_json["name"]

    assert vending_machine_id_got == 1 and vending_machine_name_got == "vending1"


def test_service_vending_machine_location_wrong_arg(client: FlaskClient):
    sample_param = {"random_location": "my_house"}
    get_all_vending_machine_at_location_response = client.get(ENDPOINT + "/machine-stock", query_string=sample_param)

    assert get_all_vending_machine_at_location_response.status_code == 200

    json_response_got = get_all_vending_machine_at_location_response.json

    json_success_response = json_response_got["success"]

    assert not json_success_response
