from flask import Flask, jsonify

app = Flask(__name__)

USERS = [
    {"id": 1, "nome": "Alice"},
    {"id": 2, "nome": "Bruno"},
    {"id": 3, "nome": "Carla"},
]

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(USERS)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "users"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)