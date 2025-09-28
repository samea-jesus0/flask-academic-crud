from model.database import db
from model.professor import Professor

class ProfessorController:
    @staticmethod
    def index():
        professores = Professor.query.all()
        return professores

    @staticmethod
    def delete(id):
        professor = Professor.query.filter_by(id=id).first()
        if professor:
            db.session.delete(professor)
            db.session.commit()