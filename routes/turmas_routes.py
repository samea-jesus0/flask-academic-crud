from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash
from controller.turma_controller import TurmaController
from controller.professor_controller import ProfessorController
from model.turma import Turma
from model.database import db
from datetime import datetime

turmas_bp = Blueprint("turma_rota", __name__, url_prefix="/turma")

"""
definitions:
  Professor:
    type: object
    properties:
      id:
        type: integer
        description: ID único do professor.
        example: 1
      nome:
        type: string
        description: Nome completo do professor.
        example: "Dr. Carlos Andrade"
      idade:
        type: integer
        description: Idade do professor.
        example: 45
      materia:
        type: string
        description: Matéria principal que o professor leciona.
        example: "Matemática Avançada"
      observacoes:
        type: string
        description: Quaisquer observações ou notas adicionais sobre o professor.
        example: "Coordenador do departamento de ciências exatas."
  Turma:
    type: object
    properties:
      id:
        type: integer
        description: ID único da turma.
        example: 101
      descricao:
        type: string
        description: Descrição ou nome da turma.
        example: "3º Ano B - Matutino"
      professor_id:
        type: integer
        description: ID do professor responsável pela turma.
        example: 5
      ativo:
        type: boolean
        description: Indica se a turma está ativa ou não.
        example: true
  Aluno:
    type: object
    properties:
      id:
        type: integer
        description: ID do aluno.
      nome:
        type: string
        description: Nome completo do aluno.
      idade:
        type: integer
        description: Idade do aluno.
      turma_id:
        type: integer
        description: ID da turma à qual o aluno pertence.
      data_nascimento:
        type: string
        format: date
        description: Data de nascimento do aluno (YYYY-MM-DD).
      nota_primeiro_semestre:
        type: number
        format: float
        description: Nota do primeiro semestre.
      nota_segundo_semestre:
        type: number
        format: float
        description: Nota do segundo semestre.
      media_final:
        type: number
        format: float
        description: Média final do aluno.
"""

@turmas_bp.route("/")
def listar_turmas():
    """Lista todas as turmas
    Esta rota exibe uma página HTML com a lista de todas as turmas e professores cadastrados.
    ---
    tags:
      - Turmas
    responses:
      200:
        description: Uma lista de turmas.
        schema:
          type: array
          items:
            $ref: '#/definitions/Turma'
      500:
        description: Erro interno no servidor.
    """
    turmas = TurmaController.index()
    professores = ProfessorController.index()
    return render_template("turmas.html", turmas=turmas, professores=professores, titulo="Lista de Turmas")

@turmas_bp.route("/cadastrar")
def cadastrar_turma():
    """Exibe o formulário de cadastro de nova turma
    ---
    tags:
      - Turmas
    responses:
      200:
        description: Página HTML com o formulário para criar uma nova turma.
    """
    professores = ProfessorController.index()
    return render_template("cadastro_turma.html", titulo="Cadastrar Turmas", professores=professores)

@turmas_bp.route("/criar_turma", methods=["POST"])
def criar_turma():
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
        description: ID do professor selecionado para a turma.
      - name: ativo
        in: formData
        type: boolean
        description: Marque se a turma estiver ativa. O valor enviado é 'on'.
    responses:
      302:
        description: Redireciona para a lista de turmas após o sucesso na criação.
      400:
        description: Dados do formulário inválidos.
    """
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
    professores = ProfessorController.index()
    turma = Turma.query.filter_by(descricao=descricao).first()
    if not turma:
        flash("Turma não encontrada!")
        return redirect(url_for("listar_turmas"))

    if request.method == "POST":
        turma.descricao = request.form["descricao"]
        turma.professor_id = int(request.form["professor"])
        turma.ativo = "ativo" in request.form

        db.session.commit()
        flash("Turma atualizada!")
        return redirect(url_for("turma_rota.listar_turmas"))

    return render_template("cadastro_turma.html", titulo="Editar Turma", turma=turma, professores=professores)



@turmas_bp.route("/deletar/<descricao>")
def deletar_turma(descricao):
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
    turma = Turma.query.filter_by(descricao=descricao).first()
    if turma:
        TurmaController.delete(turma.id)
        flash("Turma deletada!")
    return redirect(url_for('turma_rota.listar_turmas'))
