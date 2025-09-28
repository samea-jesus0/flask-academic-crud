from model.database import db

class Professor(db.Model):
    __tablename__ = "professores"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    materia = db.Column(db.String(100), nullable=True)
    observacoes = db.Column(db.Text, nullable=True)

    turmas = db.relationship("Turma")

