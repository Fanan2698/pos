from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length, URL, Email
from flask_babel import lazy_gettext as _l

class CreateApplicationProfile(FlaskForm):
    logo = FileField(_l("Application Logo"), validators=[FileAllowed(["png", "jpg", "jpeg"], _l("Images Only"))])
    name = StringField(_l("Application Name *"), validators=[DataRequired(), Length(2,18)])
    meta_title = StringField(_l("Meta Title"))
    meta_description = TextAreaField(_l("Meta Description"))
    meta_keywords = StringField(_l("Meta Keyword"))
    button = SubmitField(_l("Save"))
