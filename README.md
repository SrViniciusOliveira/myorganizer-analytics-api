# 📊 MyOrganizer Analytics API

API desenvolvida com Flask para registrar e contabilizar visualizações de projetos, incluindo geração de badge SVG para GitHub.

---

# 🚀 Tecnologias Utilizadas

* Python
* Flask
* Flask-Limiter
* Flask-CORS
* SQLite
* dotenv

---

# 🔒 Recursos de Segurança

* Rate Limiting
* Proteção anti-spam
* Validação de parâmetros
* Controle de visualizações por IP
* Bloqueio de múltiplas visualizações em 24h
* Sanitização de entrada
* Cache para badge SVG

---

# 📁 Estrutura do Projeto

```bash
.
├── app.py
├── database.db
├── .env
├── requirements.txt
└── README.md
```

---

# ⚙️ Instalação

## 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/myorganizer-analytics-api.git
```

## 2. Entre na pasta

```bash
cd myorganizer-analytics-api
```

## 3. Crie ambiente virtual

```bash
python -m venv venv
```

## 4. Ative o ambiente virtual

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

---

# 📦 Instale as dependências

```bash
pip install -r requirements.txt
```

---

# ▶️ Executando a API

```bash
python app.py
```

Servidor iniciará em:

```bash
http://localhost:5000
```

---

# 🌐 Endpoints

---

## 🏠 Home

### GET /

Retorna status da API.

### Resposta

```json
{
  "message": "MyOrganizer Analytics API online"
}
```

---

## 📈 Contar Visualizações

### GET /analytics/<project>

Retorna quantidade de visualizações do projeto.

### Exemplo

```bash
GET /analytics/myorganizer
```

### Resposta

```json
{
  "visualizacoes": 12
}
```

---

## 👁 Registrar Visualização

### POST /visualizacao/<project>

Registra visualização única por IP durante 24 horas.

### Exemplo

```bash
POST /visualizacao/myorganizer
```

### Resposta

```json
{
  "message": "visualizacao registrada"
}
```

---

## 🟢 Badge SVG para GitHub

### GET /badge/<project>

Gera badge SVG dinâmica para README.

### Exemplo

```html
<img src="https://SEU-DOMINIO.onrender.com/badge/myorganizer" />
```

---

# 🧠 Funcionamento

A API:

* Armazena visualizações em SQLite
* Identifica usuários pelo IP
* Evita spam de visualizações
* Limita requisições automaticamente
* Gera badges SVG em tempo real

---

# 🛡 Rate Limit

## Global

```txt
100 requests por hora
```

## Registrar Visualização

```txt
10 requests por minuto
```

## Badge

```txt
30 requests por minuto
```

---

# 💾 Banco de Dados

Tabela criada automaticamente:

```sql
CREATE TABLE IF NOT EXISTS visualizador_projetos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_projeto TEXT,
    ip TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

# ☁️ Deploy

A API pode ser hospedada em:

* Render
* Railway
* VPS Linux
* Docker
* Heroku

---

# 📌 Exemplo de Uso no Frontend

```javascript

await fetch("https://SEU-DOMINIO.onrender.com/visualizacao/myorganizer", {
  method: "POST"
});

const response = await fetch(
  "https://SEU-DOMINIO.onrender.com/analytics/myorganizer"
);

const data = await response.json();

console.log(data.visualizacoes);
```

---

# 📄 Licença

MIT License

---

# 👨‍💻 Autor

Desenvolvido por Vinicius Gabriel.


