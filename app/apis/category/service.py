from flask import current_app

from app.utils import err_resp, message, internal_err_resp
from app.mod_category.models import ProductCategory

class CategoryService:
    @staticmethod
    def get_category_data(id):
        """ Get category data by slug """
        category = ProductCategory.get_by_id(id)
        if not category:
            return err_resp("Category not found!", "category_404", 404)

        from .utils import load_data

        try:
            category_data = load_data(category)

            resp = message(True, "Category data sent")
            resp["category"] = category_data
            return resp, 200
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
            
    @staticmethod
    def list_category_data():
        """ Get category data """
        category = ProductCategory.gets()
        if not category:
            return err_resp("Category not found!", "category_404", 404)

        from .utils import load_data

        try:
            resp = message(True, "Category data sent")
            resp["category"] = [load_data(x) for x in category]
            return resp, 200
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
