from app.util.sql_translate import SQLParser

sql_parser = SQLParser("products", ["product_id", "name"])


def test_select_all_every_columns():
    assert sql_parser.select_all() == "SELECT * FROM products"


def test_select_all_specific_columns():
    assert sql_parser.select_all("name") == "SELECT name FROM products"


def test_select_with_conditions_all():
    assert sql_parser.select_with_condition("name = 1") == "SELECT * FROM products WHERE name = 1"


def test_delete_record():
    assert sql_parser.delete_record("name = 2") == "DELETE FROM products WHERE name = 2"


def test_add_record():
    assert sql_parser.add_record(["1", "oreo"]) == "INSERT INTO products(product_id,name) VALUES(1,oreo)"


def test_edit_record_every_column():
    assert sql_parser.edit_record(["nutella"], "name=1") == "UPDATE products SET name=nutella WHERE name=1"
