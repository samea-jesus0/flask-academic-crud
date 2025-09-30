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
    'contact': {
        'name': 'Seu Nome',
        'email': 'seu@email.com'
    },
    'license': {
        'name': 'MIT',
    }
}
swagger = Swagger(app)

@app.route('/')
def pagina_inicial():
    return render_template('pagina_inicial.html')

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(host="0.0.0.0", port=5000)