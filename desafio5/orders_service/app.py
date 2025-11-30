from flask import Flask, jsonify

app = Flask(__name__)

ORDERS = [
    {"id": 11, "user_id": 1, "produto": "Notebook"},
    {"id": 12, "user_id": 2, "produto": "Monitor"},
    {"id": 13, "user_id": 3, "produto": "Teclado"},
]

@app.route("/orders", methods=["GET"])
def get_orders():
    return jsonify(ORDERS)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "orders"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)