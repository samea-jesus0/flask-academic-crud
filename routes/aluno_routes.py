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

"""
definitions:
  Turma:
    type: object
    properties:
      id:
        type: integer
        description: ID da turma.
      descricao:
        type: string
        description: Descrição ou nome da turma.
      professor_id:
        type: integer
        description: ID do professor associado.
      ativo:
        type: boolean
        description: Status da turma.
  Professor:
    type: object
    properties:
      id:
        type: integer
      nome:
        type: string
"""

@alunos_bp.route("/")
def listar_alunos():
    """Lista todas as turmas e professores
    Esta rota exibe uma página HTML com a lista de todas as turmas cadastradas.
    ---
    tags:
      - Turmas
    responses:
      200:
        description: Página com a lista de turmas e o formulário de cadastro.
        schema:
          type: array
          items:
            $ref: '#/'
      500:
        description: Erro interno no servidor.
    """
    alunos = AlunoController.index()
    return render_template("alunos.html", alunos=alunos, titulo="Lista de Alunos")

@alunos_bp.route("/cadastrar")
def cadastrar_aluno():
    """Exibe o formulário de cadastro de nova turma
    ---
    tags:
      - Turmas
    responses:
      200:
        description: Página HTML com o formulário para criar uma nova turma.
      500:
        description: Erro interno no servidor.
    """
    turmas = TurmaController.index()
    return render_template("cadastro_aluno.html", turmas=turmas, titulo="Cadastrar Aluno")

@alunos_bp.route("/criar_aluno", methods=["GET", "POST"])
def criar_aluno():
    """Cria uma nova turma
    Recebe os dados do formulário e cria uma nova turma no banco de dados.
    ---
    tags:
      - Turmas
    parameters:
      - name: descricao
        in: formData
        type: string
        required: true
        description: Descrição ou nome da turma.
      - name: professor
        in: formData
        type: integer
        required: true
        description: ID do professor selecionado.
      - name: ativo
        in: formData
        type: boolean
        description: Marque se a turma estiver ativa.
    responses:
      302:
        description: Redireciona para a lista de turmas após a criação com sucesso.
      400:
        description: Dados do formulário inválidos.
    """
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
    """Exibe o formulário de edição (GET) ou atualiza uma turma (POST)
    ---
    tags:
      - Turmas
    parameters:
      - name: descricao
        in: path
        type: string
        required: true
        description: A descrição da turma que será editada.
      - name: descricao
        in: formData
        type: string
        description: Novo nome/descrição da turma (usado no POST).
      - name: professor
        in: formData
        type: integer
        description: Novo ID do professor (usado no POST).
      - name: ativo
        in: formData
        type: boolean
        description: Novo status da turma (usado no POST).
    responses:
      200:
        description: (GET) Retorna o formulário de edição pré-preenchido.
      302:
        description: (POST) Redireciona para a lista de turmas após a atualização.
      404:
        description: Turma não encontrada.
    """
    turmas = TurmaController.index()
    aluno = Aluno.query.filter_by(nome=nome).first()
    if not aluno:
        flash("Aluno não encontrado!")
        return redirect(url_for("listar_alunos"))

    if request.method == "POST":
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

    return render_template("cadastro_aluno.html", titulo="Editar Aluno", turmas=turmas, aluno=aluno)

@alunos_bp.route("/deletar/<nome>")
def deletar_aluno(nome):
    """Deleta uma turma
    Encontra uma turma pela descrição e a remove do banco de dados.
    ---
    tags:
      - Turmas
    parameters:
      - name: descricao
        in: path
        type: string
        required: true
        description: A descrição da turma a ser deletada.
    responses:
      302:
        description: Redireciona para a lista de turmas após a deleção.
      404:
        description: Turma não encontrada.
    """
    aluno = Aluno.query.filter_by(nome=nome).first()
    if nome:
        AlunoController.delete(aluno.id)
        flash("Aluno deletado!")
    return redirect(url_for('aluno_rota.listar_alunos'))