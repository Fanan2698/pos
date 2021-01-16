from flask import Blueprint

bp = Blueprint("mod_user", __name__, template_folder="admin_templates")

from . import routes
