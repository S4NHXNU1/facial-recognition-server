from flask import Blueprint, jsonify

scan = Blueprint("scan", __name__, url_prefix="/scan")

@scan.route("/register", methods=["POST"])
def register():
    return jsonify({"message": "successfully registered face data"}), 200

@scan.route("/recognize", methods=["POST"])
def recognize():
    return jsonify({"message": "matched"}), 200