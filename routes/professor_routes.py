from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash
from controller.professor_controller import ProfessorController
from model import professor
from model.professor import Professor
from model.database import db
from datetime import datetime

professores_bp = Blueprint("professor_rota", __name__, url_prefix="/professor")

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
"""

@professores_bp.route("/")
def listar_professores():
    """Lista todos os professores
    Esta rota exibe uma página HTML com a lista de todos os professores cadastrados.
    ---
    tags:
      - Professores
    responses:
      200:
        description: Uma lista de professores.
        schema:
          type: array
          items:
            $ref: '#/definitions/Professor'
      500:
        description: Erro interno no servidor.
    """
    professores = ProfessorController.index()
    return render_template("professores.html", professores=professores, titulo="Lista de Professores")

@professores_bp.route("/cadastrar")
def cadastrar_professor():   
    """Exibe o formulário de cadastro de novo professor
    ---
    tags:
      - Professores
    responses:
      200:
        description: Página HTML com o formulário para criar um novo professor.
    """
    return render_template("cadastro_professor.html", titulo="Cadastrar Professores")

@professores_bp.route("/criar_professor", methods=["POST"])
def criar_professor():
    """Cria um novo professor
    Recebe os dados do formulário e cria um novo professor no banco de dados.
    ---
    tags:
      - Professores
    parameters:
      - name: nome
        in: formData
        type: string
        required: true
        description: Nome completo do professor.
      - name: idade
        in: formData
        type: integer
        required: true
        description: Idade do professor.
      - name: materia
        in: formData
        type: string
        required: true
        description: Matéria que o professor leciona.
      - name: observacoes
        in: formData
        type: string
        description: Observações adicionais.
    responses:
      302:
        description: Redireciona para a lista de professores após a criação bem-sucedida.
      400:
        description: Dados do formulário inválidos.
    """
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
    """Exibe o formulário de edição (GET) ou atualiza um professor (POST)
    ---
    tags:
      - Professores
    parameters:
      - name: nome
        in: path
        type: string
        required: true
        description: O nome do professor a ser editado.
      - name: nome
        in: formData
        type: string
        description: Novo nome do professor (usado no POST).
      - name: idade
        in: formData
        type: integer
        description: Nova idade do professor (usado no POST).
      - name: materia
        in: formData
        type: string
        description: Nova matéria do professor (usado no POST).
      - name: observacoes
        in: formData
        type: string
        description: Novas observações (usado no POST).
    responses:
      200:
        description: (GET) Retorna o formulário de edição preenchido.
      302:
        description: (POST) Redireciona para a lista de professores após a atualização.
      404:
        description: Professor não encontrado.
    """
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
    """Deleta um professor
    Encontra um professor pelo nome e o remove do banco de dados.
    ---
    tags:
      - Professores
    parameters:
      - name: nome
        in: path
        type: string
        required: true
        description: O nome do professor a ser deletado.
    responses:
      302:
        description: Redireciona para a lista de professores após a deleção.
      404:
        description: Professor não encontrado.
    """
    professor = Professor.query.filter_by(nome=nome).first()
    if professor:
        ProfessorController.delete(professor.id)
        flash("Professor deletado!")
    return redirect(url_for('professor_rota.listar_professores'))

