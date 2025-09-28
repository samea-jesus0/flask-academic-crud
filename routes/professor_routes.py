from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash
from controller.professor_controller import ProfessorController
from model import professor
from model.professor import Professor
from model.database import db
from datetime import datetime

professores_bp = Blueprint("professor_rota", __name__, url_prefix="/professor")

@professores_bp.route("/")
def listar_professores():
    professores = ProfessorController.index()
    return render_template("professores.html", professores=professores, titulo="Lista de Professores")

@professores_bp.route("/cadastrar")
def cadastrar_professor():
    return render_template("cadastro_professor.html", titulo="Cadastrar Professores")

@professores_bp.route("/criar_professor", methods=["POST"])
def criar_professor():
    novo_professor = Professor(
        nome=request.form["nome"],
        idade=int(request.form["idade"]),
        materia=request.form["materia"],
        observacoes=request.form["observacoes"]
    )
    db.session.add(novo_professor)
    db.session.commit()
    flash("Professor criado com sucesso!")
    return redirect(url_for("professor_rota.listar_professores"))

@professores_bp.route("/editar/<nome>", methods=["GET", "POST"])
def editar_professor(nome):
    professor = Professor.query.filter_by(nome=nome).first()
    if not professor:
        flash("Aluno não encontrado!")
        return redirect(url_for("listar_professores"))

    if request.method == "POST":
        professor.nome = request.form["nome"]
        professor.idade = int(request.form["idade"])
        professor.materia = request.form["materia"]
        professor.observacoes = request.form["observacoes"]

        db.session.commit()
        flash("Professor atualizado!")
        return redirect(url_for("professor_rota.listar_professores"))

    return render_template("cadastro_professor.html", titulo="Editar Professor", professor=professor)



@professores_bp.route("/deletar/<nome>")
def deletar_professor(nome):
    professor = Professor.query.filter_by(nome=nome).first()
    if nome:
        ProfessorController.delete(professor.id)
        flash("Professor deletado!")
    return redirect(url_for('professor_rota.listar_professores'))