from flask_restx import Namespace, fields
from ..category.dto import CategoryDto

category = CategoryDto.category

class ProductDto:
    api = Namespace('products', description='Products related operation')

    product = api.model('Product', {
        'product_id': fields.Integer(required=True, description='Product identifier'),
        'product_photo_filename': fields.String(required=False, description='Filename product images'),
        'product_photo_path': fields.String(required=False, description='Images path of Product'),
        'product_name': fields.String(required=True, description='Name of Product'),
        'product_price': fields.Float(required=True, description='Price of Product'),
        'product_stock': fields.Integer(required=True, description='Quantity stock of Product'),
        'product_status': fields.Boolean(required=True, description='Product available status'),
        'product_slug': fields.String(required=False, description='Slug of Product'),
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
        'category_id': fields.Integer(description='Product Category'),
    })

    data_resp = api.model("Product data response", {
        "status": fields.Boolean,
        "message": fields.String,
        "product": fields.Nested(product),
    })
