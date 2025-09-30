from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash
from controller.turma_controller import TurmaController
from controller.professor_controller import ProfessorController
from model.turma import Turma
from model.database import db
from datetime import datetime

turmas_bp = Blueprint("turma_rota", __name__, url_prefix="/turma")

@turmas_bp.route("/")
def listar_turmas():
    turmas = TurmaController.index()
    professores = ProfessorController.index()
    return render_template("turmas.html", turmas=turmas, professores=professores, titulo="Lista de Turmas")

@turmas_bp.route("/cadastrar")
def cadastrar_turma():
    professores = ProfessorController.index()
    return render_template("cadastro_turma.html", titulo="Cadastrar Turmas", professores=professores)

@turmas_bp.route("/criar_turma", methods=["POST"])
def criar_turma():
    nova_turma = Turma(
        descricao=request.form["descricao"],
        professor_id=int(request.form["professor"]),
        ativo= "ativo" in request.form
    )
    db.session.add(nova_turma)
    db.session.commit()
    flash("Turma criada com sucesso!")
    return redirect(url_for("turma_rota.listar_turmas"))

@turmas_bp.route("/editar/<descricao>", methods=["GET", "POST"])
def editar_turma(descricao):
    turma = Turma.query.filter_by(descricao=descricao).first()
    if not turma:
        flash("Turma não encontrada!")
        return redirect(url_for("listar_turmas"))

    if request.method == "POST":
        turma.descricao = request.form["descricao"],
        turma.professor_id = int(request.form["professor"]),
        turma.ativo = "ativo" in request.form

        db.session.commit()
        flash("Turma atualizada!")
        return redirect(url_for("turma_rota.listar_turmas"))

    return render_template("cadastro_turma.html", titulo="Editar Turma", turma=turma)



@turmas_bp.route("/deletar/<descricao>")
def deletar_turma(descricao):
    turma = Turma.query.filter_by(descricao=descricao).first()
    if turma:
        TurmaController.delete(turma.id)
        flash("Turma deletada!")
    return redirect(url_for('turma_rota.listar_turmas'))