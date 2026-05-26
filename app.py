from dotenv import load_dotenv
from flask import Flask, Response
from flask_cors import CORS
import sqlite3
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# Banco SQLite
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

# HOME
@app.route("/")
def home():
    return {
        "message": "MyOrganizer Analytics API online"
    }

# POST - registrar view
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

# GET - contar views
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

# 🟢 BADGE PARA GITHUB
@app.route("/badge/<project>")
def badge(project):

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM vizualizador_projetos
        WHERE nome_projeto = ?
    """, (project,))

    count = cursor.fetchone()[0]

    cursor.close()

    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="120" height="20">
  <rect width="120" height="20" fill="#555"/>
  <rect x="50" width="70" height="20" fill="#4c1"/>
  <text x="5" y="14" fill="#fff" font-size="11">views</text>
  <text x="55" y="14" fill="#fff" font-size="11">{count}</text>
</svg>
"""

    return Response(svg, mimetype="image/svg+xml")


# RUN
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)