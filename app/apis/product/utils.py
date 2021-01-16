def load_data(product_db_obj):
    from app.mod_product.schema import ProductSchema

    product_schema = ProductSchema()

    data = product_schema.dump(product_db_obj)

    return data