from model.database import db
from model.turma import Turma

class TurmaController:
    @staticmethod
    def index():
        turmas = Turma.query.all()
        return turmas

    @staticmethod
    def delete(turma):
        turma = Turma.query.get(turma.id)
        if turma:
            db.session.delete(turma)
            db.session.commit()