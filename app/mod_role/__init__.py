from flask import Blueprint

bp = Blueprint("mod_role", __name__, template_folder="role_templates")

from . import routes
