from flask import Blueprint, jsonify, request
from services.authenServices import Auth, AddUser

auth = Blueprint("auth", __name__, url_prefix="/auth")

@auth.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    res = Auth(username, password)

    if not res:
        return jsonify({"message": "invalid credentials"}), 401

    return jsonify({"message": "successfully logged in"}), 200

@auth.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"]
    password = data["password"]

    res = AddUser(username, password)

    if not res:
        return jsonify({"message": "bad request"}), 400

    return jsonify({"message": "successfully registered"}), 201