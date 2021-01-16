from datetime import datetime
import os
from flask import render_template, redirect, url_for, request, flash
from flask_security import login_required, roles_accepted
from flask_babel import _
from app.decorators import confirmation
from . import bp
from .forms import CategoryForm, CreateCategory, UpdateCategory
from .models import ProductCategory
from ..helpers import str2bool


@bp.route("/")
@login_required
@roles_accepted("Admin", "Developer")
@confirmation
def categories():
    categories = ProductCategory.gets()
    return render_template(
        "categories.html", categories=categories, title=_("Categories")
    )


@bp.route("/create", methods=["POST", "GET"])
@login_required
@roles_accepted("Admin", "Developer")
@confirmation
def create_category():
    form = CreateCategory()
    if form.validate_on_submit():
        data = ProductCategory(name=form.name.data)
        data.create()
        flash(
            _("Category with name {} successfully created".format(form.name.data)),
            "info",
        )
        return redirect(url_for(".categories"))
    return render_template("category.html", form=form, title=_("Create Category"))


@bp.route("/edit/<string:slug>", methods=["POST", "GET"])
@login_required
@roles_accepted("Admin", "Developer")
@confirmation
def edit_category(slug):
    data = ProductCategory.get(slug)
    form = UpdateCategory(data.name)
    if form.validate_on_submit():
        data.name = form.name.data
        data.update()
        flash(
            _("Category with name {} successfully updated".format(form.name.data)),
            "info",
        )
        return redirect(url_for(".categories"))
    form.name.data = data.name
    return render_template("category.html", form=form, title=_("Edit Category"))


@bp.route("/delete/<string:slug>", methods=["POST", "GET"])
@login_required
@roles_accepted("Admin", "Developer")
@confirmation
def delete_category(slug):
    ProductCategory.delete(slug)
    flash(_("Category successfully deleted"), "info")
    return redirect(url_for(".categories"))


@bp.route("/activate/<string:slug>/<value>", methods=["GET", "POST"])
@login_required
@confirmation
@roles_accepted("Developer", "Admin")
def activate_category(slug, value):
    data = ProductCategory.get(slug)
    data.active = str2bool(value)
    data.update()
    return redirect(url_for(".categories"))
