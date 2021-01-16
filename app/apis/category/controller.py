from flask_restx import Resource

from .service import CategoryService
from .dto import CategoryDto

from flask_babel import _

api = CategoryDto.api
data_resp = CategoryDto.data_resp

@api.route('/')
@api.response(200, _('Category data sucessfully sent'), data_resp)
@api.response(404, _('Category not found'))
class Category(Resource):
    @api.doc('list_category')
    def get(self):
        ''' List all category '''
        return CategoryService.list_category_data()

@api.route('/<int:id>')
@api.param('id', 'The category identifier')
@api.response(200, 'Category data sucessfully sent', data_resp)
@api.response(404, 'Category not found')
class GetCategory(Resource):
    @api.doc('get_category')
    def get(self, id):
        ''' Get category by slug'''
        return CategoryService.get_category_data(id)        