from app import ma
from .models import ProductCategory

class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=ProductCategory
        include_relationships = True
        load_instance=True