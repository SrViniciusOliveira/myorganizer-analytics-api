from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
import sqlite3

load_dotenv()

app = Flask(__name__)
CORS(app)

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS vizualizador_projetos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_projeto TEXT
)
""")

conn.commit()

print("SQLite conectado!")

# HOME (apenas 1 vez)
@app.route("/")
def home():
    return {
        "message": "MyOrganizer Analytics API online"
    }

# POST view
@app.route("/analytics/<project>", methods=["POST"])
def registrar_visualizacao(project):

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO vizualizador_projetos(nome_projeto)
        VALUES (?)
    """, (project,))

    conn.commit()

    cursor.close()

    return {"message": "visualizacao registrada"}

# GET views
@app.route("/analytics/<project>", methods=["GET"])
def get_visualizacoes(project):

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM vizualizador_projetos
        WHERE nome_projeto = ?
    """, (project,))

    count = cursor.fetchone()[0]

    cursor.close()

    return {"visualizacoes": count}

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)