import json

from flask import Blueprint, Response, request, jsonify

from app.database import mysql
from app.util.api import API
from app.routes.purchase import purchase_api

listing_bp = Blueprint("listing", __name__, url_prefix="/")

listing_api = API("listing", mysql)

DEFAULT_LISTING_ARGS_MESSAGE = "Arguments needed: [vending_machine_id, product_id]"


@listing_bp.route("listing/all", methods=["GET"])
def all_listing() -> tuple[Response, int]:
    """List all the listings in the database in JSON format."""
    return listing_api.get_all_items("SELECT * FROM listing")


@listing_bp.route("/listing", methods=["GET"])
def listing() -> tuple[Response, int]:
    """Get a listing in the database in JSON format based on the vending machine and product."""
    vending_machine_id: str = request.args.get("vending_machine_id", type=str)
    product_id: str = request.args.get("product_id", type=str)
    if None in [vending_machine_id, product_id]:
        return jsonify(success=False, message=DEFAULT_LISTING_ARGS_MESSAGE), 400
    return listing_api.get_unique_item(f"product_id = {product_id} AND vending_machine_id = {vending_machine_id}")


@listing_bp.route("/listing/buy", methods=["POST"])
def purchase_listing() -> tuple[Response, int]:
    """Purchase a certain listing by one."""
    vending_machine_id: str = request.args.get("vending_machine_id", type=str)
    product_id: str = request.args.get("product_id", type=str)
    if None in [product_id, vending_machine_id]:
        return jsonify(success=False, message=DEFAULT_LISTING_ARGS_MESSAGE), 400
    query_statement: str = (
        f"UPDATE listing SET quantity = quantity - 1 WHERE product_id = {product_id} "
        f"AND vending_machine_id = {vending_machine_id}"
    )
    listing_response = listing_api.get_unique_item(
        f"product_id = {product_id} AND " f"vending_machine_id = {vending_machine_id}"
    )
    listing_response_json = listing_response[0].json
    quantity = listing_response_json["quantity"]
    create_purchase(vending_machine_id, product_id, quantity - 1)
    return listing_api.edit_item(
        query_statement, f"product_id = {product_id} AND vending_machine_id = {vending_machine_id}"
    )


@listing_bp.route("/listing/delete", methods=["POST"])
def delete_listing() -> tuple[Response, int]:
    """Delete a listing from the database."""
    vending_machine_id: str = request.args.get("vending_machine_id", type=str)
    product_id: str = request.args.get("product_id", type=str)
    if None in [product_id, vending_machine_id]:
        return jsonify(success=False, message=DEFAULT_LISTING_ARGS_MESSAGE), 400
    query_statement: str = (
        f"DELETE FROM listing WHERE product_id = {product_id} AND vending_machine_id = {vending_machine_id}"
    )
    create_purchase(vending_machine_id, product_id, "0")
    return listing_api.delete_item(query_statement)


@listing_bp.route("/listing/create", methods=["POST"])
def create_listing() -> tuple[Response, int]:
    """Create a new listing."""
    vending_machine_id: str = request.args.get("vending_machine_id", type=str)
    product_id: str = request.args.get("product_id", type=str)
    quantity: str = request.args.get("quantity", type=str)
    if None in [vending_machine_id, product_id, quantity]:
        return jsonify(success=False, message="Arguments needed: [vending_machine_id, product_id, quantity]"), 400
    query_statement = (
        f"INSERT INTO listing(product_id, vending_machine_id, quantity) "
        f"VALUES({product_id},{vending_machine_id},{quantity})"
    )
    response = listing_api.create_item(query_statement)
    create_purchase(vending_machine_id, product_id, quantity)
    return response


@listing_bp.route("/listing/edit", methods=["POST"])
def edit_listing() -> tuple[Response, int]:
    """Edit a listing in the database."""
    vending_machine_id: str = request.args.get("vending_machine_id", type=str)
    product_id: str = request.args.get("product_id", type=str)
    quantity: str = request.args.get("quantity", type=str)
    if None in [product_id, vending_machine_id, quantity]:
        return jsonify(success=False, message="Arguments needed: [vending_machine_id, product_id, quantity]"), 400
    query_statement = (
        f"UPDATE listing SET product_id = {product_id}, vending_machine_id = {vending_machine_id}, "
        f"quantity = {quantity} WHERE product_id = {product_id} "
        f"AND vending_machine_id = {vending_machine_id}"
    )
    create_purchase(vending_machine_id, product_id, quantity)
    return listing_api.edit_item(
        query_statement, f"product_id = {product_id} AND vending_machine_id = {vending_machine_id}"
    )


def create_purchase(vending_machine_id: str, product_id: str, quantity: str) -> tuple[Response, int]:
    """Create a new purchase."""
    if None in [vending_machine_id, product_id, quantity]:
        return jsonify(success=False, message="Arguments needed: [vending_machine_id, product_id, quantity]"), 400
    stock_state_response = listing_api.get_all_items(
        f"SELECT * FROM listing " f"WHERE vending_machine_id = {vending_machine_id}"
    )
    stock_state_response_json = stock_state_response[0].json
    stock_state = json.dumps(stock_state_response_json)
    query_statement = (
        f"INSERT INTO purchase(time_stamp, vending_machine_id, product_id, quantity, stock_state) "
        f"VALUES(now(),{vending_machine_id},{product_id},{quantity},'{stock_state}')"
    )
    purchase_api.create_item(query_statement)
