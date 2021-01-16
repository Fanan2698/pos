from flask import Blueprint

bp = Blueprint("mod_product", __name__, template_folder="product_templates")

from . import routes
