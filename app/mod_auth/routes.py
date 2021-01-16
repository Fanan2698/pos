from flask import render_template, flash, redirect, url_for, request
from app import db
from app.mod_auth.forms import (
    LoginForm,
    RegistrationForm,
    ResetPasswordRequestForm,
    ResetPasswordForm,
)
from flask_security import login_required, logout_user, login_user, current_user
from app.mod_user.models import User
from werkzeug.urls import url_parse
from datetime import datetime
from app.mod_auth.email import send_password_reset_email, send_confirmation_email
from app.mod_auth import bp
from flask_babel import _


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("mod_dashboard.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get(form.username.data)
        if (
            user is not None and user.check_password(form.password.data)
        ) and user.active == False:
            flash(
                _("Your account is not active. Contact your administrator for help."),
                "warning",
            )
            return redirect(url_for(".login"))
        if user is None or not user.check_password(form.password.data):
            flash(_("Invalid username or password"), "warning")
            return redirect(url_for(".login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("mod_dashboard.index")
        if user.confirmed == False:
            flash(_("Email address has not been confirmed"), "warning")
            return redirect(url_for(".unconfirmed"))
        else:
            flash(_("Login Successfuly!"), "info")
        return redirect(next_page)
    return render_template("auth/login.html", title=_("Sign In"), form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash(_("Logout Successfuly!"), "info")
    return redirect(url_for(".login"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("mod_dashboard.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        data = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            active=True,
        )
        data.set_password(form.password.data)
        data.create()
        send_confirmation_email(data)
        flash(_("Confirmation email has been sent to you."), "info")
        return redirect(url_for(".login"))
    return render_template(
        "auth/register.html", title=_("Register New User"), form=form
    )


@bp.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("mod_dashboard.index"))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(_("Check your email for the instruction to reset your password"), "info")
        return redirect(url_for(".login"))
    return render_template(
        "auth/reset_password_request.html", title=_("Reset Password"), form=form
    )


@bp.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("mod_dashboard.index"))
    user = User.verify_reset_password_token(token)
    if not user:
        flash(_("Invalid or expired link"), "info")
        return redirect(url_for(".login"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_("Your password has been change"), "info")
        return redirect(url_for(".login"))
    return render_template(
        "auth/reset_password.html", form=form, title=_("Change Password")
    )


@bp.route("/confirm/<token>")
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for("mod_dashboard.index"))
    if current_user.confirm(token):
        db.session.commit()
        flash(_("You have confirmed your account."), "info")
    else:
        flash(_("The confirmation link is invalid or has expired."), "info")
    return redirect(url_for("mod_dashboard.index"))


@bp.route("/unconfirmed")
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for("mod_dashboard.index"))
    return render_template("auth/unconfirmed.html")


@bp.route("/confirm")
@login_required
def resend_confirmation():
    send_confirmation_email(current_user)
    flash(_("A new confirmation email has been sent to you."), "info")
    return redirect(url_for("mod_dashboard.index"))
