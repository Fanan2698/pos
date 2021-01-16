from flask_restx import Namespace, fields

class CategoryDto:
    api = Namespace('category', description='Category related operational')

    category = api.model('category', {
        'id': fields.Integer(required=True, description='Category identifier'),
        'name': fields.String(required=True, description='Name of Categories'),
        'active': fields.Boolean(required=True, description='Status available of Category'),
        'slug': fields.String(required=True, description='Slug of Category'),
        'created_at': fields.DateTime(),
        'updated_at': fields.DateTime(),
    })

    data_resp = api.model('category data response', {
        'status': fields.Boolean,
        'message': fields.String,
        'category': fields.Nested(category)
    })