from flask_wtf import FlaskForm
#from flask_uploads import UploadSet, IMAGES
from wtforms import StringField, SubmitField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_babel import lazy_gettext as _l
from app.mod_category.models import ProductCategory
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from .models import Product

#images = UploadSet('images', IMAGES)

def list_category():
    return ProductCategory.get_only_available()

class ProductForm(FlaskForm):
    photo = FileField(_l("Photo Product"), validators=[FileAllowed(["jpg", "png", "jpeg"], _l("Images Only"))], render_kw={"accept": ".jpg,.jpeg,.png"})
    name = StringField(_l("Product Name *"), validators=[DataRequired(), Length(4, 32)])
    category = QuerySelectField(
        _l("Category *"),
        validators=[DataRequired()],
        query_factory=list_category,
        get_label="name",
        get_pk=lambda a: a.id,
        blank_text=_l("Select Category"),
        allow_blank=True,
    )
    price = DecimalField(_l("Price *"), validators=[DataRequired(_l("Must Using Number"))])
    stock = IntegerField(_l("Stock *"), validators=[DataRequired(_l("Must Using Number"))])

class CreateProduct(ProductForm):
    save = SubmitField(_l("Save"))

    def validate_name(self, name):
        product_name = Product.get_by_name(self.name.data)
        if product_name is not None:
            raise ValidationError(_l("Product {} already available. Please use another name".format(self.name.data)))

class UpdateProduct(ProductForm):
    save = SubmitField(_l("Update"))

    def __init__(self, original_name, *args, **kwargs):
        super(UpdateProduct, self).__init__(*args, **kwargs)
        self.original_name = original_name

    def validate_name(self, name):
        if name.data != self.original_name:
            product_name = Product.get_by_name(self.name.data)
            if product_name is not None:
                raise ValidationError(_l("Product {} already available. Please use another name".format(self.name.data)))
