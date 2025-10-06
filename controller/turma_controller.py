from model.database import db
from model.turma import Turma

class TurmaController:
    @staticmethod
    def index():
        turmas = Turma.query.all()
        return turmas

    @staticmethod
    def delete(id):
        turma = Turma.query.filter_by(id=id).first()
            
        if turma.alunos:
            raise Exception("Não é possível deletar a turma porque existem alunos nela.")
        db.session.delete(turma)
        db.session.commit()
        return True
    