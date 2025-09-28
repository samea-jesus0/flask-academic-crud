from model.database import db
from model.turma import Turma

class Aluno(db.Model):
    __tablename__ = "alunos"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    nota_primeiro_semestre =db.Column(db.Float,nullable=True)
    nota_segundo_semestre =db.Column(db.Float, nullable=True)
    media_final = db.Column(db.Float, nullable=True)

    turma_id = db.Column(db.Integer, db.ForeignKey("turmas.id"), nullable=False)
    turma = db.relationship("Turma")
