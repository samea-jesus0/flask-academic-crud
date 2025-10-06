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
        if professor.turmas:
            raise Exception("Não é possível deletar professor que possui turmas.")
        
        db.session.delete(professor)
        db.session.commit()
        return True 