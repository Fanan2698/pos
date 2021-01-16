from flask import Blueprint

bp = Blueprint("mod_auth", __name__, template_folder="auth_templates")

from app.mod_auth import routes
