from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World! This Flask app is running inside a Docker container."


if __name__ == "__main__":
    # host="0.0.0.0" is required inside Docker so the app accepts
    # connections coming from outside the container (your browser).
    app.run(host="0.0.0.0", port=5000, debug=True)