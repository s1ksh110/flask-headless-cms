# app/routes.py

from flask import Blueprint

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return "Hello from the CMS!"
