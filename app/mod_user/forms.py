from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    TextAreaField,
    SelectField,
    PasswordField,
)
from wtforms.fields.html5 import EmailField, DateField, TelField, IntegerField
from wtforms.validators import (
    DataRequired,
    ValidationError,
    Length,
    Email,
    URL,
    EqualTo,
    Optional,
)
from flask_wtf.file import FileRequired, FileField, FileAllowed
from .models import User
from app.mod_role.models import Role
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_login import current_user
from flask_babel import lazy_gettext as _l


def list_role():
    return Role.query.filter(Role.name != "Developer")

class ProfileForm(FlaskForm):
    title = SelectField(
        _l("Title"), choices=[(g, g) for g in User.title.property.columns[0].type.enums]
    )
    first_name = StringField(
        _l("First name *"), validators=[DataRequired(), Length(4, 32)]
    )
    last_name = StringField(
        _l("Last name *"), validators=[DataRequired(), Length(4, 32)]
    )
    username = StringField(_l("Username *"), validators=[DataRequired(), Length(4, 32)])
    email = EmailField(
        _l("Email *"), validators=[DataRequired(), Length(4, 64), Email()]
    )
    gender = SelectField(
        _l("Gender"),
        choices=[(g, g) for g in User.gender.property.columns[0].type.enums],
    )
    bornday = DateField(_l("Day of birth"), validators=[Optional()])
    contact = TelField(_l("Phone number"))
    id_card = IntegerField(_l("No KTP"), validators=[Optional()])
    address = TextAreaField(_l("Address"), validators=[Length(min=0, max=256)])
    about_me = TextAreaField(_l("About me"), validators=[Length(min=0, max=140)])
    account_name = StringField(_l("Owner bank name"), validators=[Length(0, 64)])
    account_number = IntegerField(_l("Owner bank number"), validators=[Optional()])
    bank_name = StringField(_l("Bank name"), validators=[Length(0, 12)])
    branch = StringField(_l("Bank branch"), validators=[Length(0, 24)])
    tax_id = IntegerField(_l("No NPWP"), validators=[Optional()])


class EditProfileForm(ProfileForm):
    submit = SubmitField(_l("Save"))

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, field):
        if field.data != self.original_username:
            user = User.get(field.data)
            if user:
                raise ValidationError(
                    _l(
                        "{} has been register. Please use another username".format(
                            field.data
                        )
                    )
                )

    def validate_email(self, field):
        if field.data != self.original_email:
            user = User.get_by_email(field.data)
            if user:
                raise ValidationError(
                    _l(
                        "{} has been register. Please use another email address".format(
                            field.data
                        )
                    )
                )


class EditSelectedProfileForm(ProfileForm):
    role = QuerySelectField(
        _l("Role *"),
        query_factory=list_role,
        get_label="name",
        get_pk=lambda a: a.id,
        blank_text=_l("Select role"),
        allow_blank=True,
    )
    submit = SubmitField(_l("Save"))

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditSelectedProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.get(self.username.data)
            if user:
                raise ValidationError(
                    _l(
                        "{} has been register. Please use another username".format(
                            self.username.data
                        )
                    )
                )

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.get_by_email(self.email.data)
            if user:
                raise ValidationError(
                    _l(
                        "{} has been register. Please use another email address".format(
                            self.email.data
                        )
                    )
                )


class EditSelectedProfileForAdminForm(ProfileForm):
    role = QuerySelectField(
        _l("Role *"),
        query_factory=list_role,
        get_label="name",
        get_pk=lambda a: a.id,
        blank_text=_l("Select role"),
        allow_blank=True,
    )
    submit = SubmitField(_l("Save"))

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditSelectedProfileForAdminForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.get(self.username.data)
            if user:
                raise ValidationError(
                    _l(
                        "{} has been register. Please use another username".format(
                            self.username.data
                        )
                    )
                )

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.get_by_email(self.email.data)
            if user:
                raise ValidationError(
                    _l(
                        "{} has been register. Please use another email address".format(
                            self.email.data
                        )
                    )
                )


class CreateUserForm(ProfileForm):
    role = QuerySelectField(
        _l("Role *"),
        query_factory=list_role,
        get_label="name",
        get_pk=lambda a: a.id,
        blank_text=_l("Select role"),
        allow_blank=True,
    )
    password = PasswordField(
        _l("Password *"), validators=[DataRequired(), Length(4, 32)]
    )
    password2 = PasswordField(
        _l("Verify Password *"),
        validators=[DataRequired(), EqualTo("password"), Length(8)],
    )
    submit = SubmitField(_l("Save"))

    def validate_username(self, username):
        user = User.get(self.username.data)
        if user is not None:
            raise ValidationError(
                _l(
                    "{} has been register. Please use another username".format(
                        self.username.data
                    )
                )
            )

    def validate_email(self, email):
        user = User.get_by_email(self.email.data)
        if user is not None:
            raise ValidationError(
                _l(
                    "{} has been register. Please use another email address".format(
                        self.email.data
                    )
                )
            )


class CreateUserForAdminForm(ProfileForm):
    role = QuerySelectField(
        _l("Role *"),
        query_factory=list_role,
        get_label="name",
        get_pk=lambda a: a.id,
        blank_text=_l("Select role"),
        allow_blank=True,
    )
    password = PasswordField(
        _l("Password *"), validators=[DataRequired(), Length(4, 32)]
    )
    submit = SubmitField(_l("Save"))

    def validate_username(self, username):
        user = User.get(self.username.data)
        if user is not None:
            raise ValidationError(
                _l(
                    "{} has been register. Please use another username".format(
                        self.username.data
                    )
                )
            )

    def validate_email(self, email):
        user = User.get_by_email(self.email.data)
        if user is not None:
            raise ValidationError(
                _l(
                    "{} has been register. Please use another email address".format(
                        self.email.data
                    )
                )
            )


class PasswordForm(FlaskForm):
    old_password = PasswordField(
        _l("Old password *"), validators=[DataRequired(), Length(5, 24)]
    )
    new_password = PasswordField(
        _l("New password *"), validators=[DataRequired(), Length(5, 24)]
    )
    confirm_password = PasswordField(
        _l("Confirm new password *"),
        validators=[
            DataRequired(),
            EqualTo("new_password", _l("Password do not match")),
            Length(5, 24),
        ],
    )
    submit = SubmitField(_l("Save"))

    def validate_old_password(self, old_password):
        if not current_user.check_password(self.old_password.data):
            raise ValidationError(_l("Wrong Old Password!"))
