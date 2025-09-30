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
        if turma:
            db.session.delete(turma)
            db.session.commit()