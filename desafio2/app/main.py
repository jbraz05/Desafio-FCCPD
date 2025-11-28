import sqlite3

con = sqlite3.connect("/data/banco.db")
cur = con.cursor()

cur.execute("SELECT * FROM usuarios")
rows = cur.fetchall()

print("Usuários cadastrados no banco:")
for r in rows:
    print(r)

con.close()