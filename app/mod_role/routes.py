from app import db
from flask import redirect, render_template, flash, url_for, request, abort
from . import bp
from .models import Role
from datetime import datetime
from flask_security import login_required, roles_accepted, roles_required
from flask_babel import _
from ..decorators import confirmation


@bp.route("/")
@login_required
@roles_accepted("Developer")
@confirmation
def roles():
    roles = Role.gets()
    return render_template("roles/roles.html", roles=roles, title=_("Role"))
