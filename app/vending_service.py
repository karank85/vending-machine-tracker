from api import get_all_items
from flask import Blueprint, Response, request

vending_service_bp = Blueprint("vending_service", __name__, url_prefix="/")


@vending_service_bp.route("/service/machine-stock", methods=["GET"])
def vending_machine_stock() -> Response:
    """Get all the products provided by a vending machine."""
    vending_id: str = request.args.get("id", type=str)
    query_statement: str = f"SELECT product_id, quantity FROM listing " f"WHERE vending_machine_id = {vending_id}"
    return get_all_items(query_statement)


@vending_service_bp.route("/service/location-machine", methods=["GET"])
def location_vending_machine() -> Response:
    """Get all the vending machines installed at a location."""
    location: str = request.args.get("location", type=str)
    query_statement: str = f"SELECT vending_machine_id, name " f"FROM vending_machine WHERE location = '{location}'"
    return get_all_items(query_statement)
