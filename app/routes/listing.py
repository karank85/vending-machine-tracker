from flask import Blueprint, Response, request, jsonify

from app.database import mysql
from app.util.api import API

listing_bp = Blueprint("listing", __name__, url_prefix="/")

listing_api = API("listing", mysql)

DEFAULT_LISTING_ARGS_MESSAGE = "Arguments needed: [vending_machine_id, product_id]"


@listing_bp.route("listing/all", methods=["GET"])
def all_listing() -> Response:
    """List all the listings in the database in JSON format."""
    return listing_api.get_all_items("SELECT * FROM listing")


@listing_bp.route("/listing", methods=["GET"])
def listing() -> Response:
    """Get a listing in the database in JSON format based on the vending machine and product."""
    try:
        vending_machine_id: str = request.args.get("vending_machine_id", type=str)
        product_id: str = request.args.get("product_id", type=str)
        return listing_api.get_unique_item(f"product_id = {product_id} AND vending_machine_id = {vending_machine_id}")
    except ValueError:
        return jsonify(success=False, message=DEFAULT_LISTING_ARGS_MESSAGE)


@listing_bp.route("/listing/buy", methods=["POST"])
def purchase_listing() -> Response:
    """Purchase a certain listing by one."""
    try:
        vending_machine_id: str = request.args.get("vending_machine_id", type=str)
        product_id: str = request.args.get("product_id", type=str)
        query_statement: str = (
            f"UPDATE listing SET quantity = quantity - 1 WHERE product_id = {product_id} "
            f"AND vending_machine_id = {vending_machine_id}"
        )
        return listing_api.edit_item(
            query_statement, f"product_id = {product_id} AND vending_machine_id = {vending_machine_id}"
        )
    except ValueError:
        return jsonify(success=False, message=DEFAULT_LISTING_ARGS_MESSAGE)


@listing_bp.route("/listing/delete", methods=["POST"])
def delete_listing() -> Response:
    """Delete a listing from the database."""
    try:
        vending_machine_id: str = request.args.get("vending_machine_id", type=str)
        product_id: str = request.args.get("product_id", type=str)
        query_statement: str = (
            f"DELETE FROM listing WHERE product_id = {product_id} AND vending_machine_id = {vending_machine_id}"
        )
        return listing_api.delete_item(query_statement)
    except ValueError:
        return jsonify(success=False, message=DEFAULT_LISTING_ARGS_MESSAGE)


@listing_bp.route("/listing/create", methods=["POST"])
def create_listing() -> Response:
    """Create a new listing."""
    try:
        vending_machine_id: str = request.args.get("vending_machine_id", type=str)
        product_id: str = request.args.get("product_id", type=str)
        quantity: str = request.args.get("quantity", type=str)
        query_statement = (
            f"INSERT INTO listing(product_id, vending_machine_id, quantity) "
            f"VALUES({product_id},{vending_machine_id},{quantity})"
        )
        return listing_api.create_item(query_statement)
    except ValueError:
        return jsonify(success=False, message="Arguments needed: [vending_machine_id, product_id, quantity]")


@listing_bp.route("/listing/edit", methods=["POST"])
def edit_listing() -> Response:
    """Edit a listing in the database."""
    try:
        vending_machine_id: str = request.args.get("vending_machine_id", type=str)
        product_id: str = request.args.get("product_id", type=str)
        quantity: str = request.args.get("quantity", type=str)
        query_statement = (
            f"UPDATE listing SET product_id = {product_id}, vending_machine_id = {vending_machine_id}, "
            f"quantity = {quantity} WHERE product_id = {product_id} "
            f"AND vending_machine_id = {vending_machine_id}"
        )
        return listing_api.edit_item(
            query_statement, f"product_id = {product_id} AND vending_machine_id = {vending_machine_id}"
        )
    except ValueError:
        return jsonify(success=False, message="Arguments needed: [vending_machine_id, product_id, quantity]")
