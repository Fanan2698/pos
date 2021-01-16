from app import db
from slugify import slugify
from sqlalchemy import event
from datetime import datetime

class ProductCategory(db.Model):
    __tablename__ = "product_category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(124))
    active = db.Column(db.Boolean, default=True)
    slug = db.Column(db.String(256), unique=True)
    created_at = db.Column(db.DateTime(), default=datetime.now())
    updated_at = db.Column(db.DateTime())
    products = db.relationship('Product', backref='category', lazy=True)

    def __repr__(self):
        """
        Representation function
        """
        return "<Category {}>".format(self.name)

    @staticmethod
    def generate_slug(target, value, oldvalue, initiator):
        """
        For generate slug
        """
        if slugify and (not target.slug or value != oldvalue):
            target.slug = slugify(value)

    @staticmethod
    def get(param):
        """
        Get category by name.
        @param is category name.
        """
        return ProductCategory.query.filter_by(slug=param).first()

    @staticmethod
    def get_by_id(param):
        """
        Get category by name.
        @param is category name.
        """
        return ProductCategory.query.filter_by(id=param).first()

    @staticmethod
    def gets():
        """
        Get All Category Data.
        """
        return ProductCategory.query.order_by(ProductCategory.created_at.desc()).all()

    @staticmethod
    def get_all_only_available():
        """
        Get All Category Data.
        """
        return ProductCategory.query.filter_by(active=True).order_by(ProductCategory.created_at.desc()).all()

    @staticmethod
    def get_by_name(param):
        """
        Get product category data by @param
        @param is name of product category
        """
        return ProductCategory.query.filter_by(name=param.lower()).first()

    @staticmethod
    def get_only_available():
        """
        Get All Category Data.
        """
        return ProductCategory.query.filter_by(active=True).order_by(ProductCategory.name.desc()).all()

    def create(self):
        """
        Create data from self and commit.
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Update category.
        """
        db.session.commit()

    @staticmethod
    def delete(param):
        """
        Delete category by name.
        @param is name of category
        """
        data = ProductCategory.get(param)
        db.session.delete(data)
        db.session.commit()

event.listen(ProductCategory.name, "set", ProductCategory.generate_slug, retval=False)
