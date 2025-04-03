from flask import Blueprint, jsonify

auth = Blueprint("auth", __name__, url_prefix="/auth")

@auth.route("/", methods=["GET"])
def index():
    return jsonify({"message": "this is auth route"}), 200