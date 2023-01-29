import random

import requests

ENDPOINT = "http://127.0.0.1:5000/"


def vending_machine_get_all():
    get_all_vending_machine_response = requests.get(ENDPOINT + f"/vending-machine/all")

    assert get_all_vending_machine_response.status_code == 200

    return get_all_vending_machine_response.json()


def test_vending_machine_get_unique():
    sample_param = {'id': '2'}
    get_a_single_product = requests.get(ENDPOINT + f"vending-machine", params=sample_param)

    assert get_a_single_product.status_code == 200

    json_response_got = get_a_single_product.json()

    vending_machine_id_got = json_response_got["vending_machine_id"]
    vending_machine_name_got = json_response_got["name"]
    location_got = json_response_got["location"]

    assert vending_machine_id_got == 2 and vending_machine_name_got == "vending2" and location_got == "old building"


def test_vending_machine_get_no_key_exist():
    sample_fake_param = {'id': '9000'}

    get_a_single_vending_machine_response = requests.get(ENDPOINT + f"vending-machine", params=sample_fake_param)

    assert get_a_single_vending_machine_response.status_code == 200

    json_response_got = get_a_single_vending_machine_response.json()

    response_status_got = json_response_got["success"]

    assert not response_status_got


def test_edit_vending_machine():
    random_location_to_set = ["kfc", "burger king", "dominoes", "mcdonalds",
                              "popeyes", "chic fil a", "wingstop",
                              "taco bell", "chester grill"][random.randint(0, 8)]
    random_name_to_set = ["vending8", "vending9", "vending10", "vending11",
                          "vending12", "vending13", "vending14",
                          "vending15", "vending16"][random.randint(0, 8)]

    sample_param = {"id": '3', "name": random_name_to_set, "location": random_location_to_set}

    get_vending_machine_after_edit = requests.post(ENDPOINT + f"/vending-machine/edit", params=sample_param)

    assert get_vending_machine_after_edit.status_code == 200

    json_response_after_edit = get_vending_machine_after_edit.json()

    print(json_response_after_edit)
    name_after_edit = json_response_after_edit["name"]
    location_after_edit = json_response_after_edit["location"]

    assert name_after_edit == random_name_to_set and \
           location_after_edit == random_location_to_set


def test_delete_vending_machine():
    sample_param = {"id": '5'}

    get_listing_after_deleting = requests.post(ENDPOINT + f"/vending-machine/delete", params=sample_param)

    assert get_listing_after_deleting.status_code == 200

    json_response_after_delete = get_listing_after_deleting.json()

    assert vending_machine_get_all() == json_response_after_delete


def test_create_vending_machine():
    sample_param = {"name": 'coolvending', "location": 'mars'}
    vending_machine_create_response = requests.post(ENDPOINT + f"/vending-machine/create", params=sample_param)

    assert vending_machine_create_response.status_code == 200

    json_response_after_create = vending_machine_create_response.json()

    assert vending_machine_get_all() == json_response_after_create
