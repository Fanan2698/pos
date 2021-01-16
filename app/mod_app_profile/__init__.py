from flask import Blueprint

bp = Blueprint("mod_app_profile", __name__, template_folder="app_profile_templates")

from . import routes
