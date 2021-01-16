from app import db
from datetime import datetime
from app.mod_product.models import Product
from sqlalchemy.sql import func

class Items(db.Model):
    __tablename__ = "items"

    items_id = db.Column(db.Integer, primary_key=True)
    qty = db.Column(db.Integer)
    product_price = db.Column(db.Float)
    sub_total = db.Column(db.Float)
    sales_id = db.Column(db.Integer, db.ForeignKey('sales.sales_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))

    def __repr__(self):
        """
        Representation function
        """
        return "<Sales Item {}>".format(self.items_id)

    @staticmethod
    def get(param):
        """
        Get point of sales by name.
        @param is id of sales 
        """
        return Items.query.filter_by(items_id=param).first()

    @staticmethod
    def get_by_sales(param):
        """
        Get point of sales by name.
        @param is id of sales 
        """
        return Items.query.filter_by(sales_id=param).all()


    @staticmethod
    def gets():
        """
        Get All Category Data.
        """
        return Items.query.all()

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
        Delete point of sales by id
        @param is id
        """
        data = Items.get(param)
        db.session.delete(data)
        db.session.commit()

    def sum_of_sub_total(param):
        """
        Sum of sub_total filter by @param
        @param is saled_id
        """
        query = db.session.query(func.sum(Items.sub_total)).group_by(Items.sales_id==param).all()
        return query

    def sum_of_qty(param):
        """
        Sum of quantity filter by @param
        @param is saled_id
        """
        query = db.session.query(func.sum(Items.qty)).group_by(Items.sales_id==param).all()
        return query

class Sales(db.Model):
    __tablename__ = "sales"

    sales_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime(), default=datetime.now())
    updated_at = db.Column(db.DateTime())
    items = db.relationship('Items', backref='items', lazy=True)

    def __repr__(self):
        """
        Representation function
        """
        return "<Sales {}>".format(self.sales_id)

    @staticmethod
    def get(param):
        """
        Get point of sales by name.
        @param is id of sales 
        """
        return Sales.query.filter_by(sales_id=param).first()

    @staticmethod
    def gets():
        """
        Get All Category Data.
        """
        return Sales.query.order_by(Sales.created_at.desc()).all()

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
        Delete point of sales by id
        @param is id
        """
        data = Sales.get(param)
        db.session.delete(data)
        db.session.commit()


""" p = Product()
i = Items()
i.products.append(p)
db.session.add(i)
db.session.commit() """