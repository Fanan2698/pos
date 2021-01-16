from app import ma
from .models import Product

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=Product
        #include_relationships = True
        include_fk = True
        load_instance=True