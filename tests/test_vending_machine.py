from flask import Response
from flask.testing import FlaskClient

ENDPOINT = "/vending-machine"


def vending_machine_get_all(client: FlaskClient) -> Response:
    get_all_vending_machine_response = client.get(ENDPOINT + "/all")

    assert get_all_vending_machine_response.status_code == 200

    return get_all_vending_machine_response.json


def test_vending_machine_get_unique(client: FlaskClient):
    sample_param = {"id": "2"}
    get_a_single_product = client.get(ENDPOINT, query_string=sample_param)

    assert get_a_single_product.status_code == 200

    json_response_got = get_a_single_product.json

    vending_machine_id_got = json_response_got["vending_machine_id"]
    vending_machine_name_got = json_response_got["name"]
    location_got = json_response_got["location"]

    assert vending_machine_id_got == 2 and vending_machine_name_got == "vending2" and location_got == "old building"


def test_vending_machine_get_unique_wrong_arg(client: FlaskClient):
    sample_param = {"bigboyvending": "2"}
    get_a_single_vending_machine = client.get(ENDPOINT, query_string=sample_param)

    assert get_a_single_vending_machine.status_code == 400

    json_response_got = get_a_single_vending_machine.json

    json_success_response = json_response_got["success"]

    assert not json_success_response


def test_vending_machine_get_no_key_exist(client: FlaskClient):
    sample_fake_param = {"id": "9000"}

    get_a_single_vending_machine_response = client.get(ENDPOINT, query_string=sample_fake_param)

    assert get_a_single_vending_machine_response.status_code == 502

    json_response_got = get_a_single_vending_machine_response.json

    response_status_got = json_response_got["success"]

    assert not response_status_got


def test_edit_vending_machine(client: FlaskClient):
    sample_param_pre_edit = {
        "id": "3",
        "name": "vending100",
        "location": "panda express",
    }

    get_vending_machine_pre_edit = client.post(ENDPOINT + "/edit", query_string=sample_param_pre_edit)

    assert get_vending_machine_pre_edit.status_code == 200

    json_response_pre_edit = get_vending_machine_pre_edit.json

    name_pre_edit = json_response_pre_edit["name"]
    location_pre_edit = json_response_pre_edit["location"]

    sample_param_after_edit = {
        "id": "3",
        "name": "vending15",
        "location": "mcdonald",
    }

    get_vending_machine_after_edit = client.post(ENDPOINT + "/edit", query_string=sample_param_after_edit)

    assert get_vending_machine_after_edit.status_code == 200

    json_response_after_edit = get_vending_machine_after_edit.json

    name_after_edit = json_response_after_edit["name"]
    location_after_edit = json_response_after_edit["location"]

    assert name_after_edit != name_pre_edit and location_after_edit != location_pre_edit


def test_delete_vending_machine(client: FlaskClient):
    sample_param = {"id": "5"}

    get_vending_machine_after_deleting = client.post(ENDPOINT + "/delete", query_string=sample_param)

    assert get_vending_machine_after_deleting.status_code == 200


def test_delete_vending_machine_wrong_arg(client: FlaskClient):
    sample_param_delete = {"imgonnadeletethis": "2"}
    get_vending_machine_after_deleting = client.post(ENDPOINT + "/delete", query_string=sample_param_delete)

    assert get_vending_machine_after_deleting.status_code == 400

    json_response_got = get_vending_machine_after_deleting.json

    json_success_response = json_response_got["success"]

    assert not json_success_response


def test_create_vending_machine(client: FlaskClient):
    before_create_json = vending_machine_get_all(client)

    sample_param = {"name": "coolvending", "location": "mars"}
    vending_machine_create_response = client.post(ENDPOINT + "/create", query_string=sample_param)

    assert vending_machine_create_response.status_code == 200

    json_response_after_create = vending_machine_create_response.json

    assert before_create_json != json_response_after_create
