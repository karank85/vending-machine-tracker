from flask import Blueprint, Response, request, jsonify

from app.database import mysql
from app.util.api import API

vending_service_bp = Blueprint("vending_service", __name__, url_prefix="/")


@vending_service_bp.route("/service/machine-stock", methods=["GET"])
def vending_machine_stock() -> Response | tuple[Response, int]:
    """Get all the products provided by a vending machine."""
    listing_api: API = API("listing", mysql)
    vending_id: str = request.args.get("id", type=str)
    if vending_id is not None:
        query_statement: str = f"SELECT product_id, quantity FROM listing WHERE vending_machine_id = {vending_id}"
        return listing_api.get_all_items(query_statement)
    else:
        return jsonify(success=False, message="Arguments needed: [id]"), 400


@vending_service_bp.route("/service/location-machine", methods=["GET"])
def location_vending_machine() -> Response | tuple[Response, int]:
    """Get all the vending machines installed at a location."""
    location: str = request.args.get("location", type=str)
    if location is not None:
        vending_machine_api: API = API("vending_machine", mysql)
        query_statement: str = f"SELECT vending_machine_id, name FROM vending_machine WHERE location = '{location}'"
        return vending_machine_api.get_all_items(query_statement)
    else:
        return jsonify(success=False, message="Arguments needed: [location]"), 400
