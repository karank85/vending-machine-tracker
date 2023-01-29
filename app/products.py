from typing import Any, Callable

import MySQLdb
from config.error_message import BAD_REQUEST_MESSAGE, NO_KEY_FOUND_MESSAGE
from flask import Blueprint, Response, jsonify, request

product_bp = Blueprint("product", __name__, url_prefix="/")


def import_query_run_function() -> Callable[[str], tuple[int, Any, Any]]:
    """Import run sql script function."""
    from run_query import run_sql_script

    return run_sql_script


@product_bp.route("/product/all", methods=["GET"])
def all_products() -> Response:
    """Get all the products in the database."""
    query_run_function = import_query_run_function()

    output_rows, mysql, cur = query_run_function("SELECT * FROM products")

    if output_rows > 0:
        products: MySQLdb.cursors.CursorStoreResultMixIn = cur.fetchall()
        cur.close()
        return jsonify(products)
    return jsonify(success=False, message=NO_KEY_FOUND_MESSAGE)


@product_bp.route("/product", methods=["GET"])
def product() -> Response:
    """Get a certain product from the database provided with the id."""
    query_run_function = import_query_run_function()
    if request.method == "GET":
        product_id: str = request.args.get("id", type=str)

        output_rows, mysql, cur = query_run_function(f"SELECT * FROM products WHERE product_id={product_id}")

        if output_rows > 0:
            pdt: MySQLdb.cursors.CursorStoreResultMixIn = cur.fetchone()
            return jsonify(pdt)
        return jsonify(success=False, message=NO_KEY_FOUND_MESSAGE)
    else:
        return jsonify(success=False, message=BAD_REQUEST_MESSAGE)


@product_bp.route("/product/delete", methods=["POST"])
def delete_product() -> Response:
    """Delete a product from the database."""
    query_run_function = import_query_run_function()
    if request.method == "POST":
        product_id: str = request.args.get("id", type=str)

        output_rows, mysql, cur = query_run_function(f"DELETE FROM products WHERE product_id = {product_id}")

        mysql.connection.commit()
        cur.close()
        request.method = "GET"
        return all_products()
    else:
        return jsonify(success=False, message=BAD_REQUEST_MESSAGE)


@product_bp.route("/product/create", methods=["POST"])
def create_product() -> Response:
    """Create a new product and adding to the database with the name and price per unit."""
    query_run_function = import_query_run_function()

    if request.method == "POST":
        name: str = request.args.get("name", type=str)
        price: str = request.args.get("price", type=str)

        output_rows, mysql, cur = query_run_function(
            f"INSERT INTO products(product_name, price) VALUES('{name}',{price})"
        )

        mysql.connection.commit()
        cur.close()
        request.method = "GET"
        return all_products()
    else:
        return jsonify(success=False, message=BAD_REQUEST_MESSAGE)


@product_bp.route("/product/edit", methods=["POST"])
def edit_product() -> Response:
    """List all the listings in the database in JSON format."""
    query_run_function = import_query_run_function()
    if request.method == "POST":
        product_id: str = request.args.get("id", type=str)
        name: str = request.args.get("name", type=str)
        price: str = request.args.get("price", type=str)
        output, mysql, cur = query_run_function(
            f"UPDATE products SET product_name = '{name}', price = {price} WHERE product_id={product_id}"
        )

        mysql.connection.commit()

        if output > 0:
            cur.close()
            request.method = "GET"
            return product()
        else:
            return jsonify(success=False, message=NO_KEY_FOUND_MESSAGE)
    else:
        return jsonify(success=False, message=BAD_REQUEST_MESSAGE)
