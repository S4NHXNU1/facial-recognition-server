from flask import Blueprint, jsonify

auth = Blueprint("auth", __name__, url_prefix="/auth")

@auth.route("/login", methods=["POST"])
def login():
    return jsonify({"message": "successfully logged in"}), 200

@auth.route("/register", methods=["POST"])
def register():
    return jsonify({"message": "successfully registered"}), 201