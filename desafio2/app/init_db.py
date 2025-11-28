import sqlite3

con = sqlite3.connect("/data/banco.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
)
""")

cur.execute("INSERT INTO usuarios (nome) VALUES ('Joao')")
cur.execute("INSERT INTO usuarios (nome) VALUES ('Maria')")

con.commit()
con.close()

print("Banco inicializado com sucesso.")
