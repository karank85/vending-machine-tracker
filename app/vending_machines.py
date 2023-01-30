from api import create_item, delete_item, edit_item, get_all_items, get_unique_item
from flask import Blueprint, Response, request

vending_bp = Blueprint("vending", __name__, url_prefix="/")


@vending_bp.route("/vending-machine/all", methods=["GET"])
def all_vending_machines() -> Response:
    """List all the vending machines in the database in JSON format."""
    query_statement = "SELECT * FROM vending_machine"
    return get_all_items(query_statement)


@vending_bp.route("/vending-machine", methods=["GET"])
def vending_machine() -> Response:
    """Get information about a certain vending machine provided with the ID."""
    vending_machine_id: str = request.args.get("id", type=str)
    query_statement = f"SELECT * FROM vending_machine WHERE vending_machine_id={vending_machine_id}"
    return get_unique_item(query_statement)


@vending_bp.route("/vending-machine/delete", methods=["POST"])
def delete_vending_machine() -> Response:
    """Delete a vending machine from the database."""
    vending_machine_id: str = request.args.get("id", type=str)
    query_statement = f"DELETE FROM vending_machine WHERE vending_machine_id = {vending_machine_id}"
    return delete_item(query_statement, "vending_machine")


@vending_bp.route("/vending-machine/create", methods=["POST"])
def create_vending_machine() -> Response:
    """Create a new vending machine provided with the name and location."""
    name: str = request.args.get("name", type=str)
    location: str = request.args.get("location", type=str)
    query_statement: str = f"INSERT INTO vending_machine(location, name) VALUES('{location}','{name}')"
    return create_item(query_statement, "vending_machine")


@vending_bp.route("/vending-machine/edit", methods=["POST"])
def edit_vending_machine() -> Response:
    """Edit the vending machine information and update it into the database."""
    vending_machine_id: str = request.args.get("id", type=str)
    location: str = request.args.get("location", type=str)
    name: str = request.args.get("name", type=str)
    query_statement = (
        f"UPDATE vending_machine SET location = '{location}', name = '{name}' "
        f"WHERE vending_machine_id={vending_machine_id}"
    )
    return edit_item(query_statement, "vending_machine")
