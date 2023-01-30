from api import create_item, delete_item, edit_item, get_all_items, get_unique_item
from flask import Blueprint, Response, request

listing_bp = Blueprint("listing", __name__, url_prefix="/")


@listing_bp.route("listing/all", methods=["GET"])
def all_listing() -> Response:
    """List all the listings in the database in JSON format."""
    query_statement: str = "SELECT * FROM listing"
    return get_all_items(query_statement)


@listing_bp.route("/listing", methods=["GET"])
def listing() -> Response:
    """Get a listing in the database in JSON format based on the vending machine and product."""
    vending_machine_id: str = request.args.get("vending_machine_id", type=str)
    product_id: str = request.args.get("product_id", type=str)
    query_statement: str = (
        f"SELECT * FROM listing WHERE product_id = {product_id} AND vending_machine_id = {vending_machine_id}"
    )
    return get_unique_item(query_statement)


@listing_bp.route("/listing/buy", methods=["POST"])
def purchase_listing() -> Response:
    """Purchase a certain listing by one."""
    vending_machine_id: str = request.args.get("vending_machine_id", type=str)
    product_id: str = request.args.get("product_id", type=str)
    query_statement: str = (
        f"UPDATE listing SET quantity = quantity - 1 WHERE product_id = {product_id} "
        f"AND vending_machine_id = {vending_machine_id}"
    )
    return edit_item(query_statement, "listing")


@listing_bp.route("/listing/delete", methods=["POST"])
def delete_listing() -> Response:
    """Delete a listing from the database."""
    vending_machine_id: str = request.args.get("vending_machine_id", type=str)
    product_id: str = request.args.get("product_id", type=str)
    query_statement: str = (
        f"DELETE FROM listing WHERE product_id = {product_id} AND vending_machine_id = {vending_machine_id}"
    )
    return delete_item(query_statement, "listing")


@listing_bp.route("/listing/create", methods=["POST"])
def create_listing() -> Response:
    """Create a new listing."""
    vending_machine_id: str = request.args.get("vending_machine_id", type=str)
    product_id: str = request.args.get("product_id", type=str)
    quantity: str = request.args.get("quantity", type=str)
    query_statement = (
        f"INSERT INTO listing(product_id, vending_machine_id, quantity) "
        f"VALUES({product_id},{vending_machine_id},{quantity})"
    )
    return create_item(query_statement, "listing")


@listing_bp.route("/listing/edit", methods=["POST"])
def edit_listing() -> Response:
    """Edit a listing in the database."""
    vending_machine_id: str = request.args.get("vending_machine_id", type=str)
    product_id: str = request.args.get("product_id", type=str)
    quantity: str = request.args.get("quantity", type=str)
    query_statement = (
        f"UPDATE listing SET product_id = {product_id}, vending_machine_id = {vending_machine_id}, "
        f"quantity = {quantity} WHERE product_id = {product_id} "
        f"AND vending_machine_id = {vending_machine_id}"
    )
    return edit_item(query_statement, "listing")
