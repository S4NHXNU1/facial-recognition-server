from flask import Blueprint, jsonify

scan = Blueprint("scan", __name__, url_prefix="/scan")

@scan.route("/", methods=["GET"])
def index():
    return jsonify({"message": "this is scan route"}), 200