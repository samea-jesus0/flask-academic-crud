from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from routes.aluno_routes import alunos_bp
from routes.professor_routes import professores_bp
from routes.turmas_routes import turmas_bp
from model.database import db
from flasgger import Swagger

app = Flask(__name__)
app.secret_key = 'jogoteca'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///escola.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

app.register_blueprint(alunos_bp)
app.register_blueprint(professores_bp)
app.register_blueprint(turmas_bp)

app.config['SWAGGER'] = {
    'title': 'API de Gestão Acadêmica',
    'uiversion': 3,
    'version': '1.0.0',
    'description': 'Documentação da API para gerenciar turmas e professores.',
    'termsOfService': '/termos',
    'license': {
        'name': 'MIT',
    }
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "API Escolar",
        "description": "API para gerenciar professores, turmas e alunos.",
        "version": "1.0.0"
    },
    "definitions": {
        "Professor": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "description": "ID único do professor.", "example": 1},
                "nome": {"type": "string", "description": "Nome completo do professor.", "example": "Dr. Carlos Andrade"},
                "idade": {"type": "integer", "description": "Idade do professor.", "example": 45},
                "materia": {"type": "string", "description": "Matéria principal que o professor leciona.", "example": "Matemática Avançada"},
                "observacoes": {"type": "string", "description": "Observações adicionais sobre o professor.", "example": "Coordenador do departamento de ciências exatas."}
            },
            "required": ["id", "nome", "idade", "materia"]
        },
        "Turma": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "description": "ID único da turma.", "example": 101},
                "descricao": {"type": "string", "description": "Descrição ou nome da turma.", "example": "3º Ano B - Matutino"},
                "professor_id": {"type": "integer", "description": "ID do professor responsável pela turma.", "example": 5},
                "ativo": {"type": "boolean", "description": "Indica se a turma está ativa ou não.", "example": True}
            },
            "required": ["id", "descricao", "professor_id", "ativo"]
        },
        "Aluno": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "description": "ID do aluno.", "example": 1},
                "nome": {"type": "string", "description": "Nome completo do aluno.", "example": "João Silva"},
                "idade": {"type": "integer", "description": "Idade do aluno.", "example": 20},
                "turma_id": {"type": "integer", "description": "ID da turma à qual o aluno pertence.", "example": 101},
                "data_nascimento": {"type": "string", "format": "date", "description": "Data de nascimento do aluno (YYYY-MM-DD).", "example": "2005-06-15"},
                "nota_primeiro_semestre": {"type": "number", "format": "float", "description": "Nota do primeiro semestre.", "example": 8.5},
                "nota_segundo_semestre": {"type": "number", "format": "float", "description": "Nota do segundo semestre.", "example": 9.0},
                "media_final": {"type": "number", "format": "float", "description": "Média final do aluno.", "example": 8.75}
            },
            "required": ["id", "nome", "idade", "turma_id"]
        }
    }
}

swagger = Swagger(app, template=swagger_template)

@app.route('/')
def pagina_inicial():
    return render_template('pagina_inicial.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)