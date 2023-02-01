from config.error_message import BAD_REQUEST_MESSAGE
from database import mysql
from flask import Blueprint, Response, jsonify, request
from util.api import API

product_bp = Blueprint("product", __name__, url_prefix="/")

product_api = API("products", mysql)


@product_bp.route("/product/all", methods=["GET"])
def all_products() -> Response:
    """Get all the products in the database."""
    if request.method == "GET":
        return product_api.get_all_items("SELECT * FROM products")
    else:
        return jsonify(success=False, message=BAD_REQUEST_MESSAGE)


@product_bp.route("/product", methods=["GET"])
def product() -> Response:
    """Get a certain product from the database provided with the id."""
    if request.method == "GET":
        product_id: str = request.args.get("id", type=str)
        return product_api.get_unique_item(f"product_id={product_id}")
    else:
        return jsonify(success=False, message=BAD_REQUEST_MESSAGE)


@product_bp.route("/product/delete", methods=["POST"])
def delete_product() -> Response:
    """Delete a product from the database."""
    if request.method == "POST":
        product_id: str = request.args.get("id", type=str)
        query_statement = f"DELETE FROM products WHERE product_id = {product_id}"
        return product_api.delete_item(query_statement)
    else:
        return jsonify(success=False, message=BAD_REQUEST_MESSAGE)


@product_bp.route("/product/create", methods=["POST"])
def create_product() -> Response:
    """Create a new product and adding to the database with the name and price per unit."""
    if request.method == "POST":
        name: str = request.args.get("name", type=str)
        price: str = request.args.get("price", type=str)

        query_statement = f"INSERT INTO products(product_name, price) VALUES('{name}',{price})"
        return product_api.create_item(query_statement)
    else:
        return jsonify(success=False, message=BAD_REQUEST_MESSAGE)


@product_bp.route("/product/edit", methods=["POST"])
def edit_product() -> Response:
    """List all the listings in the database in JSON format."""
    if request.method == "POST":
        product_id: str = request.args.get("id", type=str)
        name: str = request.args.get("name", type=str)
        price: str = request.args.get("price", type=str)
        query_statement: str = (
            f"UPDATE products SET product_name = '{name}', price = {price} WHERE product_id={product_id}"
        )
        return product_api.edit_item(query_statement, f"product_id={product_id}")
    else:
        return jsonify(success=False, message=BAD_REQUEST_MESSAGE)
