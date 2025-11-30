from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

USERS_URL = os.getenv("USERS_URL", "http://users_service:6000/users")
ORDERS_URL = os.getenv("ORDERS_URL", "http://orders_service:7000/orders")

@app.route("/users")
def users():
    response = requests.get(USERS_URL)
    return jsonify(response.json())

@app.route("/orders")
def orders():
    response = requests.get(ORDERS_URL)
    return jsonify(response.json())

@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "gateway": True,
        "services": {
            "users": USERS_URL,
            "orders": ORDERS_URL
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)