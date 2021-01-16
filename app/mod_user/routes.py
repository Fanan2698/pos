from datetime import datetime
import os
from flask import render_template, redirect, url_for, request, flash, abort, current_app
from flask_security import login_required, current_user, roles_accepted
from flask_babel import _
from app.helpers import (
    allowed_file,
    unique_filename_for_user,
    delete_local_image,
    get_local_image,
    unique_filename,
    str2bool,
)
from app.decorators import confirmation
from app import db
from . import bp
from .forms import (
    EditProfileForm,
    CreateUserForm,
    CreateUserForAdminForm,
    EditSelectedProfileForm,
    EditSelectedProfileForAdminForm,
    PasswordForm,
)
from .models import User


@bp.route("/static/<filename>")
def display_image(filename):
    """
    Display image from localfile
    """
    filename = get_local_image(filename)
    return redirect(url_for("static", filename="uploads/" + filename))


@bp.before_request
def before_request():
    """
    function that call for update status login of user
    """
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route("/")
@login_required
@roles_accepted("Developer", "Admin")
@confirmation
def users():
    """
    Get All User data
    """
    if current_user.roles == ["Developer"]:
        users = User.gets()
    else:
        users = User.gets_for_user()
    return render_template("main/users/users.html", title=_("User data"), users=users)


@bp.route("/create", methods=["GET", "POST"])
@login_required
@roles_accepted("Developer", "Admin")
@confirmation
def create_user():
    """
    Create new user data
    """
    # Get Current Directory
    # directory = os.path.join(os.getcwd(), current_app.config["UPLOAD_FOLDER"])
    if current_user.roles == ["Admin"]:
        form = CreateUserForAdminForm()
    else:
        form = CreateUserForm()
    if form.validate_on_submit():
        data = User(
            username=form.username.data,
            about_me=form.about_me.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            title=form.title.data,
            email=form.email.data,
            gender=form.gender.data,
            bornday=form.bornday.data,
            contact=form.contact.data,
            id_card=form.id_card.data,
            address=form.address.data,
            account_name=form.account_name.data,
            account_number=form.account_number.data,
            bank_name=form.bank_name.data,
            branch=form.branch.data,
            tax_id=form.tax_id.data,
            roles=[form.role.data],
            active=True,
            confirmed_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            created_at=datetime.utcnow(),
        )
        data.set_password(form.password.data)
        # Photo Local Store
        # file = form.photo.data
        # if file and allowed_file(file.filename):
        #     filename = unique_filename_for_user(file, form.username.data)
        #     file.save(os.path.join(directory, filename))
        data.create()
        flash(
            _("User with username {} successfully created".format(form.username.data)),
            "info",
        )
        return redirect(url_for(".users"))
    return render_template("main/users/user.html", title=_("Create user"), form=form)


@bp.route("/<username>")
@login_required
@confirmation
def user(username):
    """
    Get User by username
    @param is username
    """
    user = User.get(username)
    posts = [
        {"author": user, "body": "Test Post 1"},
        {"author": user, "body": "Test Post 2"},
    ]
    return render_template(
        "main/users/user.html", title=_("User Panel"), user=user, posts=posts
    )


@bp.route("/profile", methods=["GET", "POST"])
@login_required
@confirmation
@roles_accepted("Developer", "Admin", "Cashier")
def personal_profile():
    """
    Get profile user for current login user.
    """
    form = EditProfileForm(current_user.username, current_user.email)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.title = form.title.data
        current_user.email = form.email.data
        current_user.gender = form.gender.data
        current_user.bornday = form.bornday.data
        current_user.contact = form.contact.data
        current_user.id_card = form.id_card.data
        current_user.address = form.address.data
        current_user.account_name = form.account_name.data
        current_user.account_number = form.account_number.data
        current_user.bank_name = form.bank_name.data
        current_user.branch = form.branch.data
        current_user.tax_id = form.tax_id.data
        current_user.updated_at = datetime.utcnow()
        current_user.update()
        flash(
            _(
                "Data {} {} successfully updated".format(
                    form.first_name.data, form.last_name.data,
                )
            ),
            "info",
        )
        return redirect(url_for(".personal_profile"))
    # else:
    #    flash(_("Failed update data. Check form error"), "danger")
    form.username.data = current_user.username
    form.about_me.data = current_user.about_me
    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    form.title.data = current_user.title
    form.email.data = current_user.email
    form.gender.data = current_user.gender
    form.bornday.data = current_user.bornday
    form.contact.data = current_user.contact
    form.id_card.data = current_user.id_card
    form.address.data = current_user.address
    form.account_name.data = current_user.account_name
    form.account_number.data = current_user.account_number
    form.bank_name.data = current_user.bank_name
    form.branch.data = current_user.branch
    form.tax_id.data = current_user.tax_id
    return render_template(
        "main/profiles/profile.html", title=_("Edit User"), form=form
    )


@bp.route("/edit/<username>", methods=["GET", "POST"])
@login_required
@confirmation
@roles_accepted("Developer", "Admin")
def edit_user(username):
    """
    @username parameter
    Edit user data by @username
    """
    # Get Current Directory
    # directory = os.path.join(os.getcwd(), current_app.config["UPLOAD_FOLDER"])
    if current_user.username == username:
        return redirect(url_for(".personal_profile"))
    elif User.query.filter_by(username=username).first().roles == ["Developer"]:
        flash(_("You do not have permission to view this resource."), "danger")
        return redirect(url_for(".users"))
    else:
        data = User.get(username)
        if current_user.roles == ["Admin"]:
            form = EditSelectedProfileForAdminForm(username, data.email)
        else:
            form = EditSelectedProfileForm(username, data.email)
        if form.validate_on_submit():
            data.username = form.username.data
            data.about_me = form.about_me.data
            data.first_name = form.first_name.data
            data.last_name = form.last_name.data
            data.title = form.title.data
            data.email = form.email.data
            data.gender = form.gender.data
            data.bornday = form.bornday.data
            data.contact = form.contact.data
            data.id_card = form.id_card.data
            data.address = form.address.data
            data.account_name = form.account_name.data
            data.account_number = form.account_number.data
            data.bank_name = form.bank_name.data
            data.branch = form.branch.data
            data.tax_id = form.tax_id.data
            data.roles = [form.role.data]
            data.updated_at = datetime.utcnow()
            # Updating Photo To Local Store
            # file = form.photo.data
            # if file is not None:
            #    if file and allowed_file(file.filename):
            #        filename = unique_filename_for_user(file, form.username.data)
            #        if os.path.isfile(
            #            current_app.config["UPLOAD_FOLDER"]
            #            + get_name_image(data.username)
            #        ):
            #            delete_image(data.username)
            #            file.save(os.path.join(directory, filename))
            #        else:
            #            file.save(os.path.join(directory, filename))
            data.update()
            flash(
                _(
                    "Data {} {} successfully updated".format(
                        form.first_name.data, form.last_name.data,
                    )
                ),
                "info",
            )
            return redirect(url_for(".edit_user", username=username))
        form.username.data = data.username
        form.about_me.data = data.about_me
        form.first_name.data = data.first_name
        form.last_name.data = data.last_name
        form.title.data = data.title
        form.email.data = data.email
        form.gender.data = data.gender
        form.bornday.data = data.bornday
        form.contact.data = data.contact
        form.id_card.data = data.id_card
        form.address.data = data.address
        form.account_name.data = data.account_name
        form.account_number.data = data.account_number
        form.bank_name.data = data.bank_name
        form.branch.data = data.branch
        form.tax_id.data = data.tax_id
        [form.role.data] = data.roles
    return render_template(
        "main/users/user.html",
        title=_("Edit User"),
        user=data,
        form=form,
        username=username,
    )


@bp.route("/delete/<username>", methods=["GET", "POST"])
@login_required
@confirmation
@roles_accepted("Developer", "Admin")
def delete_user(username):
    """
    @username parameter
    Delete user by @username parameter
    """
    delete = User.delete(username)
    flash(_("Data {} successfully deleted".format(username)), "info")
    return redirect(url_for(".users"))


@bp.route("/password", methods=["GET", "POST"])
@login_required
@confirmation
def password():
    """
    Change password current user
    """
    form = PasswordForm()
    if form.validate_on_submit():
        current_user.set_password(form.new_password.data)
        current_user.update()
        flash(_("Password successfully updated"), "info")
        return redirect(url_for(".password"))
    return render_template(
        "main/password/password.html", title=_("Password"), form=form
    )


@bp.route("/activate/<username>/<value>", methods=["GET", "POST"])
@login_required
@confirmation
@roles_accepted("Developer", "Admin")
def activate_user(username, value):
    user = User.get(username)
    user.active = str2bool(value)
    user.update()
    flash(_("Status User {} sucessfully updated").format(user.username), "info")
    return redirect(url_for(".users"))
