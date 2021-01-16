from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.mod_user.models import User
from flask_babel import lazy_gettext as _l


class LoginForm(FlaskForm):
    username = StringField(_l("Username"), validators=[DataRequired(), Length(5)])
    password = PasswordField(_l("Password"), validators=[DataRequired(), Length(8)])
    remember_me = BooleanField(_l("Remember Me"))
    submit = SubmitField(_l("Sign In"))


class RegistrationForm(FlaskForm):
    first_name = StringField(
        _l("First Name *"), validators=[DataRequired(), Length(3, 24)]
    )
    last_name = StringField(_l("Last Name *"), validators=[DataRequired(), Length(3, 24)])
    username = StringField(_l("Username *"), validators=[DataRequired(), Length(5)])
    email = StringField(_l("Email *"), validators=[DataRequired(), Email()])
    password = PasswordField(_l("Password *"), validators=[DataRequired(), Length(8)])
    password2 = PasswordField(
        _l("Verify Password *"),
        validators=[DataRequired(), EqualTo("password"), Length(8)],
    )
    submit = SubmitField(_l("Register"))

    def validate_username(self, username):
        user = User.get(username.data)
        if user is not None:
            raise ValidationError(_l("Please use a different username."))

    def validate_email(self, email):
        email = User.get_by_email(email.data)
        if email is not None:
            raise ValidationError(_l("Please use a different email."))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l("Email"), validators=[DataRequired(), Email()])
    submit = SubmitField(_l("Request Password Reset"))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l("New Password"), validators=[DataRequired(), Length(8)])
    password2 = PasswordField(
        _l("Confirm Password"), validators=[DataRequired(), EqualTo("password"), Length(8)]
    )
    submit = SubmitField(_l("Change Password"))
