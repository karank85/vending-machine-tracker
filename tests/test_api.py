from flask import Response, Flask
from flask_mysqldb import MySQL

from app.util.api import API


def test_all_items(app_database: tuple[Flask, MySQL]) -> Response:
    """Get all items to help me test for other tests."""
    app, database = app_database
    with app.app_context():
        products_api = API("products", database)
        got = products_api.get_all_items("SELECT * FROM products")

        assert got[1] == 200

        return got[0]


def test_get_unique_item(app_database: tuple[Flask, MySQL]):
    app, database = app_database
    with app.app_context():
        condition_sample_input: str = "product_id = 2"
        products_api = API("products", database)
        got = products_api.get_unique_item(condition_sample_input)

        assert got[1] == 200
        got_json = got[0].json

        product_id_got = got_json["product_id"]
        product_name_got = got_json["product_name"]
        price_got = got_json["price"]

        assert product_id_got == 2 and product_name_got == "est" and price_got == 22


#
#
def test_get_unique_item_no_key(app_database: tuple[Flask, MySQL]):
    app, database = app_database
    with app.app_context():
        products_api = API("products", database)
        condition_sample_input: str = "product_id = 9000"
        got = products_api.get_unique_item(condition_sample_input)

        assert got[1] == 502

        got_json = got[0].json

        response_status_got = got_json["success"]

        assert not response_status_got


def test_create_item(app_database: tuple[Flask, MySQL]):
    app, database = app_database

    query_statement = "INSERT INTO products(product_name, price) VALUES('cheetos',80)"

    with app.app_context():
        products_api = API("products", database)
        before_create = test_all_items(app_database)

        assert before_create.status_code == 200

        before_create_json = before_create.json

        after_create_response = products_api.create_item(query_statement)[0]

        assert after_create_response.status_code == 200

        after_create_json = after_create_response.json

        assert before_create_json != after_create_json


def test_delete_item(app_database: tuple[Flask, MySQL]):
    app, database = app_database
    with app.app_context():
        products_api = API("products", database)
        before_delete = test_all_items(app_database)

        assert before_delete.status_code == 200

        before_delete_json = before_delete.json

        query_statement = "DELETE FROM products ORDER BY product_id DESC LIMIT 1"

        after_delete_response = products_api.delete_item(query_statement)[0]

        assert after_delete_response.status_code == 200

        after_delete_json = after_delete_response.json

        print(after_delete_json)

        assert before_delete_json != after_delete_json


def test_edit_item(app_database: tuple[Flask, MySQL]):
    app, database = app_database

    query_statement: str = "UPDATE products SET product_name = 'apple', price = 50 WHERE product_id=5"

    query_statement_revert_back: str = "UPDATE products SET product_name = 'banana', price = 45 WHERE product_id=5"
    with app.app_context():
        products_api = API("products", database)

        get_product_pre_edit_response = products_api.edit_item(query_statement, "product_id=5")[0]

        assert get_product_pre_edit_response.status_code == 200

        json_response_pre_edit = get_product_pre_edit_response.json

        price_pre_edit = json_response_pre_edit["price"]
        name_pre_edit = json_response_pre_edit["product_name"]

        get_product_after_edit_response = products_api.edit_item(query_statement_revert_back, "product_id=5")[0]

        assert get_product_after_edit_response.status_code == 200

        json_response_after_edit = get_product_after_edit_response.json

        price_after_edit = json_response_after_edit["price"]
        name_after_edit = json_response_after_edit["product_name"]

        assert name_after_edit != name_pre_edit and price_pre_edit != price_after_edit


def test_edit_item_wrong_key(app_database: tuple[Flask, MySQL]):
    app, database = app_database

    query_statement: str = "UPDATE products SET product_name = 'apple', price = 50 WHERE product_id=600"

    with app.app_context():
        products_api = API("products", database)

        get_product_edit_response = products_api.edit_item(query_statement, "product_id=5")[0]

        assert get_product_edit_response.status_code == 200

        json_response = get_product_edit_response.json

        json_response_success = json_response["success"]

        assert not json_response_success
