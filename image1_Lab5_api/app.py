
from flask import Flask, request, jsonify
from flask_cors import CORS

from database import (
    create_db_table,
    get_users,
    get_user_by_id,
    insert_user,
    update_user,
    patch_user,
    delete_user
)

app = Flask(__name__)
CORS(app)

create_db_table()

USER_FIELDS = ("name", "email", "phone", "address", "country")


# GET ALL USERS
@app.route("/api/users", methods=["GET"])
def api_get_users():
    return jsonify(get_users()), 200


# GET A SINGLE USER
@app.route("/api/users/<int:user_id>", methods=["GET"])
def api_get_user(user_id):
    user = get_user_by_id(user_id)

    if user is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user), 200


# ADD A NEW USER
@app.route("/api/users/add", methods=["POST"])
def api_add_user():
    user = request.get_json(silent=True)

    if not isinstance(user, dict):
        return jsonify({"error": "A JSON object is required"}), 400

    missing = [
        field for field in USER_FIELDS
        if not isinstance(user.get(field), str)
        or not user[field].strip()
    ]

    if missing:
        return jsonify({
            "error": "Missing or invalid fields",
            "fields": missing
        }), 400

    new_user = insert_user(user)

    return jsonify(new_user), 201


# UPDATE AN ENTIRE USER
@app.route("/api/users/update", methods=["PUT"])
def api_update_user():
    user = request.get_json(silent=True)

    if not isinstance(user, dict):
        return jsonify({"error": "A JSON object is required"}), 400

    if type(user.get("user_id")) is not int:
        return jsonify({"error": "A valid user_id is required"}), 400

    missing = [
        field for field in USER_FIELDS
        if not isinstance(user.get(field), str)
        or not user[field].strip()
    ]

    if missing:
        return jsonify({
            "error": "Missing or invalid fields",
            "fields": missing
        }), 400

    updated = update_user(user)

    if updated is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify(updated), 200


# PARTIALLY UPDATE A USER
@app.route("/api/users/<int:user_id>", methods=["PATCH"])
def api_patch_user(user_id):
    changes = request.get_json(silent=True)

    if not isinstance(changes, dict) or not changes:
        return jsonify({"error": "JSON fields are required"}), 400

    invalid = [
        field for field, value in changes.items()
        if field not in USER_FIELDS
        or not isinstance(value, str)
        or not value.strip()
    ]

    if invalid:
        return jsonify({
            "error": "Invalid fields",
            "fields": invalid
        }), 400

    updated = patch_user(user_id, changes)

    if updated is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify(updated), 200


# DELETE A USER
@app.route("/api/users/delete/<int:user_id>", methods=["DELETE"])
def api_delete_user(user_id):
    deleted = delete_user(user_id)

    if not deleted:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "status": "User deleted successfully"
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
