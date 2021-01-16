from flask_restx import Resource

from .service import ProductService
from .dto import ProductDto

api = ProductDto.api
data_resp = ProductDto.data_resp

@api.route('/')
@api.response(200, 'Product data successfully sent', data_resp)
@api.response(404, 'Product not found')
class ProductList(Resource):
    @api.doc('list_product')
    def get(self):
        '''List all products'''
        return ProductService.list_product_data()

@api.route('/<int:id>')
@api.param('id', 'The product identifier')
@api.response(200, 'Product data successfully sent', data_resp)
@api.response(404, 'Product not found')
class Product(Resource):
    @api.doc('get_product')
    def get(self, id):
        '''Fetch a product given its identifier'''
        return ProductService.get_product_data(id)