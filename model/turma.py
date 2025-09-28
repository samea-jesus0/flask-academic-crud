from model.database import db

class Turma(db.Model):
    __tablename__ = "turmas"
    id = db.Column(db.Integer, primary_key=True)
    observacoes = db.Column(db.Text, nullable=True)
    data_nascimento = db.Column(db.Date, nullable=False)
    nota_primeiro_semestre =db.Column(db.Float,nullable=True)
    nota_segundo_semestre =db.Column(db.Float, nullable=True)
    media_final = db.Column(db.Float, nullable=True)

    alunos = db.relationship("Aluno", back_populates="turma")

    professor_id = db.Column(db.Integer, db.ForeignKey("professores.id"), nullable=False)
    professor = db.relationship("Professor", back_populates="turmas")