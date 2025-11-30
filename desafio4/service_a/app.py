from flask import Flask, jsonify

app = Flask(__name__)

USERS = [
    {"id": 1, "nome": "Alice", "ativo_desde": "2023-01-10"},
    {"id": 2, "nome": "Bruno", "ativo_desde": "2022-07-05"},
    {"id": 3, "nome": "Carla", "ativo_desde": "2021-03-18"},
]


@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(USERS)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "A"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)