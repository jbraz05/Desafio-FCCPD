from flask import Flask
import os
import psycopg2
import redis

app = Flask(__name__)

redis_client = redis.Redis(host=os.getenv("REDIS_HOST"), port=6379)

conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST")
)

@app.route("/")
def index():

    redis_client.incr("visits")
    visits = redis_client.get("visits").decode()

    cur = conn.cursor()
    cur.execute("SELECT texto FROM mensagens LIMIT 1;")
    row = cur.fetchone()
    mensagem = row[0] if row else "Sem mensagem"

    return {
        "mensagem": mensagem,
        "visitas": visits,
        "status": "comunicacao ok entre web, db e redis"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)