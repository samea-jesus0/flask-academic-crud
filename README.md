
## 🎯 Projeto: API de Gerenciamento Escolar

Este projeto consiste em uma **API REST em Flask** estruturada no padrão **MVC**, com CRUD para **Professores, Turmas e Alunos**, persistência em banco de dados **SQLite** via **SQLAlchemy**, documentação automática em **Swagger** e aplicação conteinerizada em **Docker**.

- Para criar uma turma é necessário existir pelo menos um professor e para criar um aluno é preciso ter uma turma existente.

---

## 🛠️ Tecnologias utilizadas

* [Flask](https://flask.palletsprojects.com/)
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
* [Flasgger (Swagger UI)](https://github.com/flasgger/flasgger)
* [SQLite](https://www.sqlite.org/)
* [Docker](https://www.docker.com/)

---

## 📂 Estrutura do Projeto (MVC)

```
/projeto
│── app.py                # Ponto de entrada da aplicação
│── requirements.txt       # Dependências
│── Dockerfile             # Configuração do container
│── /model                 # Modelos do banco (SQLAlchemy)
│    ├── database.py
│    ├── professor.py
│    ├── turma.py
│    └── aluno.py
│── /controller            # Regras de negócio
│    ├── professor_controller.py
│    ├── turma_controller.py
│    └── aluno_controller.py
│── /routes                # Rotas da API
│    ├── professor_routes.py
│    ├── turma_routes.py
│    └── aluno_routes.py
│── /static                # Arquivos estáticos (se necessário)
│── /templates             # Templates HTML (se necessário)
└── README.md              # Documentação
```

---

## 🚀 Como rodar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/flask-mvc-api.git
cd flask-mvc-api
```

### 2. Criar e ativar ambiente virtual (opcional, se não for usar Docker)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Rodar a aplicação (sem Docker)

```bash
flask run
```

A aplicação ficará disponível em: [http://localhost:5000](http://localhost:5000)

### 5. Rodar a aplicação com Docker 🐳

```bash
# Build da imagem
docker build -t flask-mvc-api .

# Rodar o container
docker run -p 5000:5000 flask-mvc-api
```

---

## 📖 Documentação da API (Swagger)

Após iniciar a aplicação, acesse:
👉 [http://localhost:5000/apidocs](http://localhost:5000/apidocs)

Lá você verá todos os endpoints organizados.

---

## 📌 Endpoints Principais

### Professores (`/professores`)

* `GET /professores` → Lista todos os professores
* `POST /professores` → Cria novo professor
* `PUT /professores/{id}` → Atualiza professor
* `DELETE /professores/{id}` → Remove professor

### Turmas (`/turmas`)

* `GET /turmas` → Lista todas as turmas
* `POST /turmas` → Cria nova turma
* `PUT /turmas/{id}` → Atualiza turma
* `DELETE /turmas/{id}` → Remove turma

### Alunos (`/alunos`)

* `GET /alunos` → Lista todos os alunos
* `POST /alunos` → Cria novo aluno
* `PUT /alunos/{id}` → Atualiza aluno
* `DELETE /alunos/{id}` → Remove aluno

---
