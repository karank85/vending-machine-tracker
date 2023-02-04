from flask import Blueprint, Response, request, jsonify

from app.database import mysql
from app.util.api import API

vending_bp = Blueprint("vending", __name__, url_prefix="/")

vending_machine_api = API("vending_machine", mysql)


@vending_bp.route("/vending-machine/all", methods=["GET"])
def all_vending_machines() -> Response:
    """List all the vending machines in the database in JSON format."""
    return vending_machine_api.get_all_items("SELECT * FROM vending_machine")


@vending_bp.route("/vending-machine", methods=["GET"])
def vending_machine() -> Response:
    """Get information about a certain vending machine provided with the ID."""
    vending_machine_id: str = request.args.get("id", type=str)
    if vending_machine_id is not None:
        return vending_machine_api.get_unique_item(f"vending_machine_id={vending_machine_id}")
    else:
        return jsonify(success=False, message="Arguments needed: [id]")


@vending_bp.route("/vending-machine/delete", methods=["POST"])
def delete_vending_machine() -> Response:
    """Delete a vending machine from the database."""
    vending_machine_id: str = request.args.get("id", type=str)
    if vending_machine_id is not None:
        query_statement = f"DELETE FROM vending_machine WHERE vending_machine_id = {vending_machine_id}"
        return vending_machine_api.delete_item(query_statement)
    else:
        return jsonify(success=False, message="Arguments needed: [id]")


@vending_bp.route("/vending-machine/create", methods=["POST"])
def create_vending_machine() -> Response:
    """Create a new vending machine provided with the name and location."""
    name: str = request.args.get("name", type=str)
    location: str = request.args.get("location", type=str)
    if None not in [name, location]:
        query_statement: str = f"INSERT INTO vending_machine(location, name) VALUES('{location}','{name}')"
        return vending_machine_api.create_item(query_statement)
    else:
        return jsonify(success=False, message="Arguments needed: [name, location]")


@vending_bp.route("/vending-machine/edit", methods=["POST"])
def edit_vending_machine() -> Response:
    """Edit the vending machine information and update it into the database."""
    vending_machine_id: str = request.args.get("id", type=str)
    location: str = request.args.get("location", type=str)
    name: str = request.args.get("name", type=str)
    if None not in [vending_machine_id, location, name]:
        query_statement = (
            f"UPDATE vending_machine SET location = '{location}', name = '{name}' "
            f"WHERE vending_machine_id={vending_machine_id}"
        )
        return vending_machine_api.edit_item(query_statement, f"vending_machine_id={vending_machine_id}")
    else:
        return jsonify(success=False, message="Arguments needed: [id, location, name]")
