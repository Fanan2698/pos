from app import db, create_app
from datetime import datetime
from flask_security import RoleMixin


class Role(db.Model, RoleMixin):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)
    updated_at = db.Column(db.DateTime(), nullable=False)

    def __repr__(self):
        return "<Role {}>".format(self.name)

    def create(self):
        """
        Create data from self and commit.
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Update data from self.
        """
        db.session.commit()

    def delete(self):
        """
        Delete data
        """
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get():
        """
        Get only single data (first)
        """
        return Role.query.first()

    @staticmethod
    def gets():
        """
        Get all data 
        """
        return Role.query.all()

    @staticmethod
    def get_data(param):
        """
        Get role by name.
        @param is role name.
        """
        return Role.query.filter_by(name=param).first_or_404()
    
    @staticmethod
    def check_if_exist():
        """
        Check if data exist or not in table roles
        """
        return Role.query.first()
