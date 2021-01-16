from flask import render_template, flash, redirect, url_for, request
from flask_security import login_required, roles_accepted
from app.mod_dashboard import bp
from flask_babel import _
from ..decorators import confirmation


@bp.route("/")
@bp.route("/dashboard")
@login_required
@confirmation
@roles_accepted("Developer", "Admin", "Cashier")
def index():
    return render_template("main/dashboard.html", title=_("Dashboard"))


@bp.route("/blank")
@login_required
@confirmation
@roles_accepted("Developer")
def blank():
    return render_template("main/blank_template.html", title=_("Blank Template"))


@bp.route("/docs/dashboard")
@login_required
@confirmation
@roles_accepted("Developer")
def docs_dashboard():
    return render_template("main/theme_docs/dashboard.html", title=_("Dashboard Docs"))


@bp.route("/docs/charts")
@login_required
@confirmation
@roles_accepted("Developer")
def docs_charts():
    return render_template("main/theme_docs/charts.html", title=_("Charts Docs"))


@bp.route("/docs/tables")
@login_required
@confirmation
@roles_accepted("Developer")
def docs_tables():
    return render_template("main/theme_docs/tables.html", title=_("Tables Docs"))


@bp.route("/docs/forms")
@login_required
@confirmation
@roles_accepted("Developer")
def docs_forms():
    return render_template("main/theme_docs/forms.html", title=_("Forms Docs"))


@bp.route("/docs/bs-element")
@login_required
@confirmation
@roles_accepted("Developer")
def docs_bs_element():
    return render_template(
        "main/theme_docs/bs_element.html", title=_("Bootstrap Element Docs")
    )


@bp.route("/docs/bs-grid")
@login_required
@confirmation
@roles_accepted("Developer")
def docs_bs_grid():
    return render_template(
        "main/theme_docs/bs_grid.html", title=_("Bootstrap Grid Docs")
    )

