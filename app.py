from flask import request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
from flask import Flask, Response
from flask_cors import CORS
import sqlite3
import re
import os



load_dotenv()

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:5173"
        ]
    }
})


limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits = ["100 per hour"]
)

# Banco SQLite
conn = sqlite3.connect("database.db", check_same_thread=False)
conn.execute("PRAGMA journal_mode=WAL;")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS visualizador_projetos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_projeto TEXT,
    ip TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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


# GET - contar views
@app.route("/analytics/<project>", methods=["GET"])
def get_visualizacoes(project):

    if len(project) > 50:
        return {"error": "nome invalido"}, 400 
    
    if not re.match(r'^[a-zA-Z0-9_-]+$', project):
        return {"error": "nome invalido"}, 400

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM visualizador_projetos
        WHERE nome_projeto = ?
    """, (project,))

    count = cursor.fetchone()[0]

    cursor.close()

    return {"visualizacoes": count}


# POST - registrar view
@app.route("/visualizacao/<project>", methods=["POST"])
@limiter.limit("10 per minute")
def registrar_visualizacao(project):

    if len(project) > 50:
        return {"error": "nome invalido"}, 400 
    
    if not re.match(r'^[a-zA-Z0-9_-]+$', project):
        return {"error": "nome invalido"}, 400

    cursor = conn.cursor()

    # Pega IP Do Usuário
    ip = request.headers.get("X-Forwarded-For") or request.remote_addr or "unknown"

    if "," in ip:
        ip = ip.split(",")[0].strip()


    # Verifica se já visualizou nas últimas 24 Horas
    cursor.execute("""
    SELECT id FROM visualizador_projetos
    WHERE nome_projeto = ?
    AND ip = ?
    AND datetime(created_at) > datetime('now', '-24 hours')
    """, (project, ip))

    exists  = cursor.fetchone()

    # Se já existe -> Não conta novamente 
    if exists:
        cursor.close()
        return {"message": "visualizacao já registrada"}
    
    # Registra nova visualizacao

    cursor.execute("""
                   INSERT INTO visualizador_projetos(nome_projeto, ip)
                   VALUES (?, ?)""", (project, ip))

    conn.commit()

    cursor.close()

    return {"message": "visualizacao registrada"}


# 🟢 BADGE PARA GITHUB
@app.route("/badge/<project>")
@limiter.limit("30 per minute")
def badge(project):

    if len(project) > 50:
        return {"error": "nome invalido"}, 400 
    
    if not re.match(r'^[a-zA-Z0-9_-]+$', project):
        return {"error": "nome invalido"}, 400

    cursor = conn.cursor()

    # APENAS CONTA AS VISUALIZAÇÕES
    cursor.execute("""
        SELECT COUNT(*)
        FROM visualizador_projetos
        WHERE nome_projeto = ?
    """, (project,))

    count = cursor.fetchone()[0]

    cursor.close()

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="130" height="20">
<rect width="130" height="20" fill="#24292e"/>
<rect x="55" width="75" height="20" fill="#2ea043"/>
<text x="10" y="14" fill="#fff" font-size="11">views</text>
<text x="70" y="14" fill="#fff" font-size="11">{count}</text>
</svg>"""

    return Response(
        svg,
        mimetype="image/svg+xml",
        headers={
            "Cache-Control": "public, max-age=300"
        }
    )

# RUN
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)