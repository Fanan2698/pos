from flask import Blueprint

bp = Blueprint("mod_bussines_profile", __name__, template_folder="profile_templates")

from . import routes
