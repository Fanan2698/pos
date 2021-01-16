from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_babel import lazy_gettext as _l
from app.mod_category.models import ProductCategory

class CategoryForm(FlaskForm):
    name = StringField(_l("Name *"), validators=[DataRequired(), Length(3, 32)])

class CreateCategory(CategoryForm):
    save = SubmitField(_l("Save"))

    def validate_name(self, name):
        category_name = ProductCategory.get_by_name(self.name.data)
        if category_name is not None:
            raise ValidationError(_l("Category {} already available. Please use another name".format(self.name.data)))

class UpdateCategory(CategoryForm):
    save = SubmitField(_l("Update"))

    def __init__(self, original_name, *args, **kwargs):
        super(UpdateCategory, self).__init__(*args, **kwargs)
        self.original_name = original_name

    def validate_name(self, name):
        if name.data != self.original_name:
            category_name = ProductCategory.get_by_name(self.name.data)
            if category_name is not None:
                raise ValidationError(_l("Category {} already available. Please use another name".format(self.name.data)))
