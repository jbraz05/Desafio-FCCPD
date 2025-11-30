from flask import Flask, jsonify
import os
import requests

app = Flask(__name__)

SERVICE_A_URL = os.getenv("SERVICE_A_URL", "http://service_a:5000")


@app.route("/relatorio", methods=["GET"])
def relatorio():
    try:
        resp = requests.get(f"{SERVICE_A_URL}/users", timeout=5)
        resp.raise_for_status()
        users = resp.json()
    except Exception as e:
        return jsonify({"erro": f"Falha ao consultar o serviço A: {e}"}), 500

    frases = [
        f"Usuário {u['nome']} ativo desde {u['ativo_desde']}."
        for u in users
    ]

    return jsonify(
        {
            "quantidade_usuarios": len(users),
            "frases": frases,
            "origem": "dados vindos do microsserviço A",
        }
    )


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "B", "service_a_url": SERVICE_A_URL})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)