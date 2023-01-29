from typing import Any, Callable

import MySQLdb.cursors
from config.error_message import BAD_REQUEST_MESSAGE, NO_KEY_FOUND_MESSAGE
from flask import Blueprint, Response, jsonify, request

vending_bp = Blueprint("vending", __name__, url_prefix="/")


def import_query_run_function() -> Callable[[str], tuple[int, Any, Any]]:
    """Import run sql script function."""
    from run_query import run_sql_script

    return run_sql_script


@vending_bp.route("/vending-machine/all", methods=["GET"])
def all_vending_machines() -> Response:
    """List all the vending machines in the database in JSON format."""
    query_run_function = import_query_run_function()

    if request.method == "GET":
        output_rows, mysql, cur = query_run_function("SELECT * FROM vending_machine")

        if output_rows > 0:
            vending_machines: MySQLdb.CursorStoreResultMixIn = cur.fetchall()
            cur.close()
            return jsonify(vending_machines)
    else:
        return jsonify(success=False, message=BAD_REQUEST_MESSAGE)


@vending_bp.route("/vending-machine", methods=["GET"])
def vending_machine() -> Response:
    """Get information about a certain vending machine provided with the ID."""
    query_run_function = import_query_run_function()

    if request.method == "GET":
        vending_machine_id: str = request.args.get("id", type=str)

        output, mysql, cur = query_run_function(
            f"SELECT * FROM vending_machine WHERE vending_machine_id={vending_machine_id}"
        )

        if output > 0:
            vm: MySQLdb.CursorStoreResultMixIn = cur.fetchone()
            return jsonify(vm)
        return jsonify(success=False, message=NO_KEY_FOUND_MESSAGE)
    else:
        return jsonify(success=False, message=BAD_REQUEST_MESSAGE)


@vending_bp.route("/vending-machine/delete", methods=["POST"])
def delete_vending_machine() -> Response:
    """Delete a vending machine from the database."""
    query_run_function = import_query_run_function()
    if request.method == "POST":
        vending_machine_id: str = request.args.get("id", type=str)

        output, mysql, cur = query_run_function(
            f"DELETE FROM vending_machine WHERE vending_machine_id = {vending_machine_id}"
        )

        mysql.connection.commit()
        cur.close()

        request.method = "GET"
        return all_vending_machines()
    else:
        return jsonify(success=False, message=BAD_REQUEST_MESSAGE)


@vending_bp.route("/vending-machine/create", methods=["POST"])
def create_vending_machine() -> Response:
    """Create a new vending machine provided with the name and location."""
    query_run_function = import_query_run_function()
    if request.method == "POST":
        name: str = request.args.get("name", type=str)
        location: str = request.args.get("location", type=str)

        output, mysql, cur = query_run_function(
            f"INSERT INTO vending_machine(location, name) VALUES('{location}','{name}')"
        )

        mysql.connection.commit()
        cur.close()
        request.method = "GET"
        return all_vending_machines()
    else:
        return jsonify(success=False, message=BAD_REQUEST_MESSAGE)


@vending_bp.route("/vending-machine/edit", methods=["POST"])
def edit_vending_machine() -> Response:
    """Edit the vending machine information and update it into the database."""
    query_run_function = import_query_run_function()

    if request.method == "POST":
        vending_machine_id: str = request.args.get("id", type=str)
        location: str = request.args.get("location", type=str)
        name: str = request.args.get("name", type=str)

        output, mysql, cur = query_run_function(
            f"UPDATE vending_machine SET location = '{location}', name = '{name}' "
            f"WHERE vending_machine_id={vending_machine_id}"
        )

        mysql.connection.commit()

        if output > 0:
            cur.close()
            request.method = "GET"
            return vending_machine()
        return jsonify(success=False, message=NO_KEY_FOUND_MESSAGE)
    else:
        return jsonify(success=False, message=BAD_REQUEST_MESSAGE)
