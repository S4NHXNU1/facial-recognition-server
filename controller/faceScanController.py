from flask import Blueprint, jsonify, request
from services.faceScanServices import StoreEmbedding, CompareEmbedding

scan = Blueprint("scan", __name__, url_prefix="/scan")

@scan.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"]
    faces_base64 = data["faces_base64"]

    res = StoreEmbedding(username, faces_base64)

    if res == 0:
        return jsonify({"message": "bad request"}), 400

    return jsonify({"message": "successfully registered user and face data"}), 200

@scan.route("/match", methods=["POST"])
def match():
    data = request.json
    username = data["username"]
    face_ebase64 = data["face_base64"]

    res, matches = CompareEmbedding(username, face_ebase64)

    if not res:
        return jsonify({"message": f"unmatched ({matches}%)"}), 401

    return jsonify({"message": f"matched ({matches}%)"}), 200