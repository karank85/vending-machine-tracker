import json

from flask import Blueprint, Response, request, jsonify

from app.database import mysql
from app.util.api import API

purchase_bp = Blueprint("purchase", __name__, url_prefix="/")

purchase_api = API("purchase", mysql)

MISSING_VENDING_MACHINE_ID_PURCHASE_ARGS_MESSAGE = "Arguments needed: [vending_machine_id,]"
MISSING_PRODUCT_ID_PURCHASE_ARGS_MESSAGE = "Arguments needed: [product_id]"


@purchase_bp.route("purchase/all", methods=["GET"])
def all_purchases() -> Response:
    """List all the purchases in the database in JSON format."""
    return purchase_api.get_all_items("SELECT * FROM purchase")


@purchase_bp.route("/purchase/vending", methods=["GET"])
def purchases_by_vending_machine() -> Response:
    """Get a purchase in the database in JSON format from given vending machine."""
    vending_machine_id: str = request.args.get("vending_machine_id", type=str)
    if None in [vending_machine_id]:
        return jsonify(success=False, message=MISSING_VENDING_MACHINE_ID_PURCHASE_ARGS_MESSAGE)
    purchase_response = purchase_api.get_all_items(  # pragma: no cover
        f"SELECT * FROM purchase WHERE vending_machine_id = {vending_machine_id}"
    )
    purchase_response_json = purchase_response.json
    for purchase in purchase_response_json:  # pragma: no cover
        purchase["stock_state"] = json.loads(purchase["stock_state"])
    return purchase_response_json  # pragma: no cover


@purchase_bp.route("/purchase/product", methods=["GET"])
def purchases_by_product() -> Response:
    """Get a purchase in the database in JSON format from given product."""
    product_id: str = request.args.get("product_id", type=str)
    if None in [product_id]:  # pragma: no cover
        return jsonify(success=False, message=MISSING_PRODUCT_ID_PURCHASE_ARGS_MESSAGE)
    return purchase_api.get_all_items(f"SELECT * FROM purchase WHERE product_id = {product_id}")
