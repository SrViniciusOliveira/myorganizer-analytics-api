
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
import psycopg
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

conn = psycopg.connect(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

print("Conectado ao PostgreSQL!")

@app.route("/analytics/<project>", methods=["POST"])
def registrar_visualizacao(project):

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO vizualizador_projetos(nome_projeto)
        VALUES (%s)
    """, (project,))

    conn.commit()

    cursor.close()

    return {"message": "visualizacao registrada"}

@app.route("/analytics/<project>", methods=["GET"])
def get_visualizacoes(project):

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM vizualizador_projetos
        WHERE nome_projeto = %s
    """, (project,))

    count = cursor.fetchone()[0]

    cursor.close()

    return {"visualizacoes": count}

if __name__ == "__main__":
    app.run(debug=True)