import requests

ENDPOINT = "http://127.0.0.1:5000/"


def test_service_vending_machine_stock():
    sample_param = {'id': '2'}
    get_all_vending_machine_stock_response = requests.get(ENDPOINT + f"/service/machine-stock", params=sample_param)

    assert get_all_vending_machine_stock_response.status_code == 200


def test_service_vending_machine_location():
    sample_param = {'location': 'mlc'}
    get_all_vending_machine_at_location_response = requests.get(ENDPOINT + f"/service/location-machine"
                                                                , params=sample_param)

    assert get_all_vending_machine_at_location_response.status_code == 200

    get_single_vending_machine_at_location_json = get_all_vending_machine_at_location_response.json()[0]

    vending_machine_id_got = get_single_vending_machine_at_location_json["vending_machine_id"]
    vending_machine_name_got = get_single_vending_machine_at_location_json["name"]

    assert vending_machine_id_got == 1 and vending_machine_name_got == "vending1"
