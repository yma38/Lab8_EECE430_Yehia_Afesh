from flask import Flask, jsonify
from flask_cors import CORS

from database import create_db_table, get_users

app = Flask(__name__)
CORS(app)

create_db_table()


# GET THE NAMES OF ALL USERS
@app.route("/get_users", methods=["GET"])
def api_get_users():
    names = [user["name"] for user in get_users()]
    return jsonify(names), 200


if __name__ == "__main__":
    # host="0.0.0.0" is required inside Docker so the app accepts
    # connections coming from outside the container (browser/Postman).
    app.run(host="0.0.0.0", port=3000, debug=True)