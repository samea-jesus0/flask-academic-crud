# 📚 Sistema Escolar em Flask

Um sistema simples para gerenciar **alunos**, **professores** e **turmas**, desenvolvido em **Flask** com **SQLAlchemy**.
Permite **criar, listar, editar e excluir** registros de alunos, professores e turmas.

---

## 🚀 Tecnologias usadas

* **Python 3**
* **Flask**
* **Flask-SQLAlchemy**
* **Jinja2 (templates HTML)**
* **Bootstrap** (estilização)

---

## 🔑 Principais Funcionalidades

### 👩‍🎓 Aluno

* Criar aluno
* Listar alunos
* Editar aluno
* Excluir aluno
* Relacionar aluno com **Turma**
* Campos extras: notas e média final

### 👨‍🏫 Professor

* Criar professor
* Listar professores
* Editar professor
* Excluir professor


### 👨‍🏫 Turma (Não concluido)

* Criar Turma
* Listar Turma
* Editar Turma
* Excluir Turma

---

## 🛠️ Exemplos de Rotas

### Aluno

* `GET /alunos` → Lista alunos
* `GET /alunos/cadastrar` → Formulário para cadastrar
* `POST /alunos/criar_aluno` → Cria aluno
* `GET|POST /alunos/editar/<nome>` → Edita aluno
* `POST /alunos/excluir/<nome>` → Exclui aluno

### Professor

* `GET /professor` → Lista professores
* `POST /professor/cadastrar` → Formulário para cadastrar
* `POST /professor/criar_professor` → Cria professor
* `GET|POST /professor/editar/<nome>` → Edita professor
* `POST /professor/excluir/<nome>` → Exclui professor

---

---

## 📦 Como rodar o projeto

1. Clonar o repositório

   ```bash
   git clone <link>
   cd projeto-escola
   ```

2. Criar ambiente virtual

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Instalar dependências

   ```bash
   pip install -r requirements.txt
   ```

4. Rodar a aplicação

   ```bash
   flask run
   ```

Acesse em: [http://localhost:5000](http://localhost:5000)

---
