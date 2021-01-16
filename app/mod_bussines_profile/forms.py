from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length, URL, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_babel import lazy_gettext as _l


class CreateBusinessProfile(FlaskForm):
    name = StringField(
        _l("Company name *"), validators=[DataRequired(), Length(2, 124)]
    )
    logo = FileField(
        _l("Company logo"),
        validators=[FileAllowed(["png", "jpg", "jpeg"], _l("Images Only"))],
    )
    address = TextAreaField(_l("Address"))
    sub_district = StringField(
        _l("Sub-district *"), validators=[DataRequired(), Length(2, 64)]
    )
    district = StringField(
        _l("District *"), validators=[DataRequired(), Length(2, 64)]
    )
    province = StringField(_l("Province *"), validators=[DataRequired(), Length(2, 64)])
    country = StringField(
        _l("State *"),
        validators=[DataRequired(), Length(2, 64)],
        render_kw={"readonly": "readonly", "value": "Indonesia"},
    )
    postal_code = StringField(_l("Postal code *"), validators=[Length(2, 12)])
    phone_number = StringField(
        _l("Phone number"), validators=[DataRequired(), Length(2, 18)]
    )
    email = StringField(_l("Email *"), validators=[Email(), Length(4, 120)])
    website = StringField(_l("Website *"), validators=[URL(), Length(4, 120)])
    instagram = StringField(_l("Instagram *"), validators=[URL()])
    youtube = StringField(_l("Youtube *"), validators=[URL()])
    twitter = StringField(_l("Twitter *"), validators=[URL()])
    facebook = StringField(_l("Facebook *"), validators=[URL()])
    submit = SubmitField(_l("Save"))
