from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash
from controller.aluno_controller import AlunoController
from controller.turma_controller import TurmaController
from controller.professor_controller import ProfessorController
from model import aluno
from model.aluno import Aluno
from model.database import db
from datetime import datetime

alunos_bp = Blueprint("aluno_rota", __name__, url_prefix="/alunos")

@alunos_bp.route("/")
def listar_alunos():
    alunos = AlunoController.index()
    return render_template("alunos.html", alunos=alunos, titulo="Lista de Alunos")

@alunos_bp.route("/cadastrar")
def cadastrar_aluno():
    turmas = TurmaController.index()
    return render_template("cadastro_aluno.html", turmas=turmas, titulo="Cadastrar Aluno")

@alunos_bp.route("/criar_aluno", methods=["GET", "POST"])
def criar_aluno():
    novo_aluno = Aluno (
        nome=request.form["nome"],
        idade = int(request.form["idade"]),
        turma_id = request.form["turmas"],
        data_nascimento = datetime.strptime(request.form["data_nasc"], "%Y-%m-%d").date(),
        nota_primeiro_semestre = float(request.form["nota_semestre_um"]),
        nota_segundo_semestre = float(request.form["nota_semestre_dois"]),
        media_final = float(request.form["media_final"])
    )

    db.session.add(novo_aluno)
    db.session.commit()
    redirect(url_for("aluno_rota.listar_alunos"))

@alunos_bp.route("/editar/<nome>", methods=["GET", "POST"])
def editar_aluno(nome):
    turmas = TurmaController.index()
    aluno = Aluno.query.filter_by(nome=nome).first()  # pega o aluno do banco
    if not aluno:
        flash("Aluno não encontrado!")
        return redirect(url_for("listar_alunos"))

    if request.method == "POST":
        # atualizar dados do aluno
        aluno.nome = request.form["nome"]
        aluno.idade = int(request.form["idade"])
        aluno.turma_id = request.form["turmas"]
        aluno.data_nascimento = request.form["data_nasc"]
        aluno.nota_primeiro_semestre = request.form["nota_semestre_um"]
        aluno.nota_segundo_semestre = request.form["nota_semestre_dois"]
        aluno.media_final = request.form["media_final"]

        db.session.commit()
        flash("Aluno atualizado!")
        return redirect(url_for("aluno_rota.listar_alunos"))

    return render_template("cadastro_aluno.html", titulo="Editar Aluno", turmas=turmas)



@alunos_bp.route("/deletar/<nome>")
def deletar_aluno(nome):
    aluno = Aluno.query.filter_by(nome=nome).first()
    if nome:
        AlunoController.delete(aluno.id)
        flash("Aluno deletado!")
    return redirect(url_for('aluno_rota.listar_alunos'))