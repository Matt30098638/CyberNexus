from flask import Blueprint, jsonify, request
from shared.database.models import Asset

assets_bp = Blueprint("assets", __name__)

@assets_bp.route("/discover", methods=["GET"])
def get_assets():
    """
    Retrieve all discovered assets with optional filters.
    """
    os_filter = request.args.get("os")
    ip_filter = request.args.get("ip_address")

    query = Asset.query
    if os_filter:
        query = query.filter(Asset.os.ilike(f"%{os_filter}%"))
    if ip_filter:
        query = query.filter(Asset.ip_address.ilike(f"%{ip_filter}%"))

    agents = query.all()
    result = [
        {
            "id": asset.id,
            "name": asset.name,
            "ip_address": asset.ip_address,
            "os": asset.os,
            "last_seen": asset.last_seen
        }
        for asset in agents
    ]
    return jsonify(result), 200
