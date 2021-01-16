def load_data(category_db_obj):
    from app.mod_category.schema import CategorySchema

    category_schema = CategorySchema()

    data = category_schema.dump(category_db_obj)

    return data