from flask import current_app

from app.utils import err_resp, message, internal_err_resp
from app.mod_product.models import Product
from app.apis.category.service import CategoryService

class ProductService:
    @staticmethod
    def get_product_data(id):
        """ Get product data by slug """
        product = Product.get_by_id(id)
        if not product:
            return err_resp("Product not found!", "product_404", 404)

        from .utils import load_data

        try:
            product_data = load_data(product)

            resp = message(True, "Product data sent")
            resp["product"] = product_data
            #resp["product"]["category"] = CategoryService.get_category_data(product.category.slug)
            return resp, 200
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def list_product_data():
        """ Get all product data """
        product = Product.gets()
        if not product:
            return err_resp("Product is empty", "product_404", 404)

        from .utils import load_data
        from app.apis.category.utils import load_data as load_data_category

        try:          
            product_data = [load_data(x) for x in product]
            #category_data = [load_data_category(x.category) for x in product]
            resp = message(True, "Product data sent")
            resp["product"] = product_data
            #resp["product"]["category"] = category_data
            
            return resp, 200
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
