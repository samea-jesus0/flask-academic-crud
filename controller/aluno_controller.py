from model.database import db
from model.aluno import Aluno


class AlunoController:
    @staticmethod
    def index():
        alunos = Aluno.query.all()
        return alunos

    @staticmethod
    def delete(id):
        aluno = Aluno.query.filter_by(id=id).first()
        if aluno:
            db.session.delete(aluno)
            db.session.commit()
