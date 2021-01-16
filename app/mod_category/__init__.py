from flask import Blueprint

bp = Blueprint("mod_category", __name__, template_folder="category_templates")

from . import routes
