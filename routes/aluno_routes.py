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

@alunos_bp.route("/")
def listar_alunos():
    """Lista todos os alunos cadastrados
    Esta rota exibe uma página HTML com a lista de todos os alunos.
    ---
    tags:
      - Alunos
    responses:
      200:
        description: Página com a lista de alunos.
        schema:
          type: array
          items:
            $ref: '#/definitions/Aluno'
      500:
        description: Erro interno no servidor.
    """
    alunos = AlunoController.index()
    return render_template("alunos.html", alunos=alunos, titulo="Lista de Alunos")

@alunos_bp.route("/cadastrar")
def cadastrar_aluno():
    """Exibe o formulário de cadastro de novo aluno
    ---
    tags:
      - Alunos
    responses:
      200:
        description: Página HTML com o formulário para criar um novo aluno.
      500:
        description: Erro interno no servidor.
    """
    turmas = TurmaController.index()
    return render_template("cadastro_aluno.html", turmas=turmas, titulo="Cadastrar Aluno")

@alunos_bp.route("/criar_aluno", methods=["GET", "POST"])
def criar_aluno():
    """Cria um novo aluno
    Recebe os dados do formulário e cria um novo aluno no banco de dados.
    ---
    tags:
      - Alunos
    parameters:
      - name: nome
        in: formData
        type: string
        required: true
        description: Nome completo do aluno.
      - name: idade
        in: formData
        type: integer
        required: true
        description: Idade do aluno.
      - name: turmas
        in: formData
        type: integer
        required: true
        description: ID da turma selecionada.
      - name: data_nasc
        in: formData
        type: string
        format: date
        required: true
        description: Data de nascimento (formato YYYY-MM-DD).
      - name: nota_semestre_um
        in: formData
        type: number
        required: true
        description: Nota do primeiro semestre.
      - name: nota_semestre_dois
        in: formData
        type: number
        required: true
        description: Nota do segundo semestre.
      - name: media_final
        in: formData
        type: number
        required: true
        description: Média final do aluno.
    responses:
      302:
        description: Redireciona para a lista de alunos após a criação com sucesso.
      400:
        description: Dados do formulário inválidos.
    """
    novo_aluno = Aluno (
        nome=request.form["nome"],
        idade = int(request.form["idade"]),
        turma_id = request.form["turma"],
        data_nascimento = datetime.strptime(request.form["data_nasc"], "%Y-%m-%d").date(),
        nota_primeiro_semestre = float(request.form["nota_semestre_um"]),
        nota_segundo_semestre = float(request.form["nota_semestre_dois"]),
        media_final = float(request.form["media_final"])
    )

    db.session.add(novo_aluno)
    db.session.commit()
    return redirect(url_for("aluno_rota.listar_alunos"))

@alunos_bp.route("/editar/<nome>", methods=["GET", "POST"])
def editar_aluno(nome):
    """Exibe o formulário de edição (GET) ou atualiza um aluno (POST)
    ---
    tags:
      - Alunos
    parameters:
      - name: nome
        in: path
        type: string
        required: true
        description: O nome do aluno que será editado.
      - name: nome
        in: formData
        type: string
        description: Novo nome do aluno (usado no POST).
      - name: idade
        in: formData
        type: integer
        description: Nova idade do aluno (usado no POST).
      - name: turmas
        in: formData
        type: integer
        description: Novo ID da turma do aluno (usado no POST).
      - name: data_nasc
        in: formData
        type: string
        format: date
        description: Nova data de nascimento (YYYY-MM-DD) (usado no POST).
      - name: nota_semestre_um
        in: formData
        type: number
        description: Nova nota do primeiro semestre (usado no POST).
      - name: nota_semestre_dois
        in: formData
        type: number
        description: Nova nota do segundo semestre (usado no POST).
      - name: media_final
        in: formData
        type: number
        description: Nova média final (usado no POST).
    responses:
      200:
        description: (GET) Retorna o formulário de edição pré-preenchido.
      302:
        description: (POST) Redireciona para a lista de alunos após a atualização.
      404:
        description: Aluno não encontrado.
    """
    turmas = TurmaController.index()
    aluno = Aluno.query.filter_by(nome=nome).first()
    if not aluno:
        flash("Aluno não encontrado!")
        return redirect(url_for("listar_alunos"))

    if request.method == "POST":
        aluno.nome = request.form["nome"]
        aluno.idade = int(request.form["idade"])
        aluno.turma_id = request.form["turma"]
        aluno.data_nascimento = datetime.strptime(request.form["data_nasc"], "%Y-%m-%d").date()
        aluno.nota_primeiro_semestre = request.form["nota_semestre_um"]
        aluno.nota_segundo_semestre = request.form["nota_semestre_dois"]
        aluno.media_final = request.form["media_final"]

        db.session.commit()
        flash("Aluno atualizado!")
        return redirect(url_for("aluno_rota.listar_alunos"))

    return render_template("cadastro_aluno.html", titulo="Editar Aluno", turmas=turmas, aluno=aluno)

@alunos_bp.route("/deletar/<nome>")
def deletar_aluno(nome):
    """Deleta um aluno
    Encontra um aluno pelo nome e o remove do banco de dados.
    ---
    tags:
      - Alunos
    parameters:
      - name: nome
        in: path
        type: string
        required: true
        description: O nome do aluno a ser deletado.
    responses:
      302:
        description: Redireciona para a lista de alunos após a deleção.
      404:
        description: Aluno não encontrado.
    """
    aluno = Aluno.query.filter_by(nome=nome).first()
    if nome:
        AlunoController.delete(aluno.id)
        flash("Aluno deletado!")
    return redirect(url_for('aluno_rota.listar_alunos'))