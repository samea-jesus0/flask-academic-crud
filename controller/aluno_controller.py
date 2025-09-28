from model.database import db
from model.aluno import Aluno


class AlunoController:
    @staticmethod
    def index():
        alunos = Aluno.query.all()
        return alunos

    @staticmethod
    def delete(aluno):
        aluno = Aluno.query.get(aluno.id)
        if aluno:
            db.session.delete(aluno)
            db.session.commit()
