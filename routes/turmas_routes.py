from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash

turmas_bp = Blueprint("turma", __name__, url_prefix="/turma")