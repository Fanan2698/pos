from flask import Blueprint, render_template

bp = Blueprint("mod_dashboard", __name__, template_folder="back_office_templates")


from . import routes
