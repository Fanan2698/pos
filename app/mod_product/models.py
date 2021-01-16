from app import db
from app.mod_category.models import ProductCategory
from slugify import slugify
from sqlalchemy import event
from datetime import datetime

class Product(db.Model):
    __tablename__="products"

    product_id = db.Column(db.Integer, primary_key=True)
    product_photo_filename = db.Column(db.String(64), unique=True)
    product_photo_path = db.Column(db.String(512), unique=True)
    product_name = db.Column(db.String(128))
    product_price = db.Column(db.Float)
    product_stock = db.Column(db.Integer, default=0)
    product_status = db.Column(db.Boolean, default=True)
    product_slug = db.Column(db.String(256), unique=True)
    created_at = db.Column(db.DateTime(), default=datetime.now())
    updated_at = db.Column(db.DateTime())
    category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'))
    items = db.relationship('Items', backref='product', lazy=True)

    def __repr__(self):
        """
        Representation function
        """
        return '<Product ID: {}, Product Name : {}>'.format(self.product_id ,self.product_name)

    @staticmethod
    def generate_slug(target, value, oldvalue, initiator):
        """
        For generate slug
        """
        if slugify and (not target.product_slug or value != oldvalue):
            target.product_slug = slugify(value)

    @staticmethod
    def get(param):
        """
        Get data only one data
        @param is slug
        """
        return Product.query.filter_by(product_slug=param).first()

    @staticmethod
    def get_by_id(param):
        """
        Get data only one data
        @param is slug
        """
        return Product.query.filter_by(product_id=param).first()

    @staticmethod
    def gets():
        """
        Get all data
        """
        return Product.query.order_by(Product.created_at.desc()).all()

    @staticmethod
    def get_all_only_available():
        """
        Get all data
        """
        return Product.query.filter_by(product_status=True).order_by(Product.created_at.desc()).all()

    @staticmethod
    def get_by_name(param):
        """
        Get product data by @param
        @param is name of product
        """
        return Product.query.filter_by(product_name=param.lower()).first()

    @staticmethod
    def get_image(param):
        """
        Get image by @param
        @param is image filename
        """
        return Product.query.filter_by(product_photo_filename=param).first_or_404()

    def create(self):
        """
        Create new product data
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updated product data
        """
        db.session.commit()

    @staticmethod
    def delete(param):
        """
        Delete data by param.
        @param is slug
        """
        data = Product.get(param)
        db.session.delete(data)
        db.session.commit()

event.listen(Product.product_name, "set", Product.generate_slug, retval=False)
