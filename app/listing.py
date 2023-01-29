from typing import Any, Callable

import MySQLdb
from config.error_message import BAD_REQUEST_MESSAGE, NO_KEY_FOUND_MESSAGE
from flask import Blueprint, Response, jsonify, request

listing_bp = Blueprint("listing", __name__, url_prefix="/")


def import_query_run_function() -> Callable[[str], tuple[int, Any, Any]]:
    """Import run sql script function."""
    from run_query import run_sql_script

    return run_sql_script


@listing_bp.route("listing/all", methods=["GET"])
def all_listing() -> Response:
    """List all the listings in the database in JSON format."""
    query_run_function = import_query_run_function()

    if request.method == "GET":

        output_rows, mysql, cur = query_run_function("SELECT * FROM listing")

        if output_rows > 0:
            listings: MySQLdb.CursorStoreResultMixIn = cur.fetchall()
            cur.close()
            return jsonify(listings)
    else:
        return jsonify(success=False, message=BAD_REQUEST_MESSAGE)


@listing_bp.route("/listing", methods=["GET"])
def listing() -> Response:
    """Get a listing in the database in JSON format based on the vending machine and product."""
    query_run_function = import_query_run_function()
    if request.method == "GET":
        vending_machine_id: str = request.args.get("vending_machine_id", type=str)
        product_id: str = request.args.get("product_id", type=str)

        output_rows, mysql, cur = query_run_function(
            f"SELECT * FROM listing WHERE product_id = {product_id} AND vending_machine_id = {vending_machine_id}"
        )

        if output_rows > 0:
            listing_fetched: MySQLdb.CursorStoreResultMixIn = cur.fetchone()
            return jsonify(listing_fetched)
        return jsonify(success=False, message=NO_KEY_FOUND_MESSAGE)
    else:
        return jsonify(success=False, message=BAD_REQUEST_MESSAGE)


@listing_bp.route("/listing/buy", methods=["POST"])
def purchase_listing() -> Response:
    """Purchase a certain listing by one."""
    query_run_function = import_query_run_function()

    if request.method == "POST":
        vending_machine_id: str = request.args.get("vending_machine_id", type=str)
        product_id: str = request.args.get("product_id", type=str)

        output_rows, mysql, cur = query_run_function(
            f"UPDATE listing SET quantity = quantity - 1 WHERE product_id = {product_id} "
            f"AND vending_machine_id = {vending_machine_id}"
        )

        mysql.connection.commit()
        cur.close()
        request.method = "GET"
        return listing()
    else:
        return jsonify(success=False, message=BAD_REQUEST_MESSAGE)


@listing_bp.route("/listing/delete", methods=["POST"])
def delete_listing() -> Response:
    """Delete a listing from the database."""
    query_run_function = import_query_run_function()

    if request.method == "POST":
        vending_machine_id: str = request.args.get("vending_machine_id", type=str)
        product_id: str = request.args.get("product_id", type=str)

        output_rows, mysql, cur = query_run_function(
            f"DELETE FROM listing WHERE product_id = {product_id} AND vending_machine_id = {vending_machine_id}"
        )

        mysql.connection.commit()
        cur.close()
        request.method = "GET"
        return all_listing()
    else:
        return jsonify(success=False, message=BAD_REQUEST_MESSAGE)


@listing_bp.route("/listing/create", methods=["POST"])
def create_listing() -> Response:
    """Create a new listing."""
    query_run_function = import_query_run_function()
    if request.method == "POST":
        vending_machine_id: str = request.args.get("vending_machine_id", type=str)
        product_id: str = request.args.get("product_id", type=str)
        quantity: str = request.args.get("quantity", type=str)

        output_rows, mysql, cur = query_run_function(
            f"INSERT INTO listing(product_id, vending_machine_id, quantity) "
            f"VALUES({product_id},{vending_machine_id},{quantity})"
        )

        mysql.connection.commit()

        cur.close()
        request.method = "GET"
        return all_listing()
    else:
        return jsonify(success=False, message=BAD_REQUEST_MESSAGE)


@listing_bp.route("/listing/edit", methods=["POST"])
def edit_listing() -> Response:
    """Edit a listing in the database."""
    query_run_function = import_query_run_function()

    if request.method == "POST":
        vending_machine_id: str = request.args.get("vending_machine_id", type=str)
        product_id: str = request.args.get("product_id", type=str)
        quantity: str = request.args.get("quantity", type=str)

        output_rows, mysql, cur = query_run_function(
            f"UPDATE listing SET product_id = {product_id}, vending_machine_id = {vending_machine_id}, "
            f"quantity = {quantity} WHERE product_id = {product_id} AND vending_machine_id = {vending_machine_id}"
        )

        mysql.connection.commit()

        if output_rows > 0:
            cur.close()
            request.method = "GET"
            return listing()
        return jsonify(success=False, message=NO_KEY_FOUND_MESSAGE)
    else:
        return jsonify(success=False, message=BAD_REQUEST_MESSAGE)
