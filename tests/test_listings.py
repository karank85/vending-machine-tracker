import requests

ENDPOINT = "http://127.0.0.1:5000/"


def test_listing_get_all():
    get_all_listing_response = requests.get(ENDPOINT + f"/listing/all")

    assert get_all_listing_response.status_code == 200


def test_listing_get_unique():
    get_a_single_listing = requests.get(ENDPOINT + f"listing", params={'product_id': '2', 'vending_machine_id': '1'})

    assert get_a_single_listing.status_code == 200

    json_response_got = get_a_single_listing.json()
    print(json_response_got)
    product_id_got = json_response_got["product_id"]
    vending_machine_got = json_response_got["vending_machine_id"]
    quantity_got = json_response_got["quantity"]

    assert product_id_got == 2 and vending_machine_got == 1 and quantity_got == 20
