from flask import current_app
from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import UserMixin, RoleMixin
from flask_login import AnonymousUserMixin
from hashlib import md5
from time import time
import jwt
from app.mod_role.models import Role
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

roles_users = db.Table(
    "roles_users",
    db.Column("id", db.Integer(), db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Enum("Mr.", "Mrs.", "Ms.", name="title"))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    gender = db.Column(db.Enum("Man", "Woman", name="gender"))
    bornday = db.Column(db.Date)
    contact = db.Column(db.String(16))
    address = db.Column(db.Text)
    id_card = db.Column(db.Integer)
    account_name = db.Column(db.String(64))
    account_number = db.Column(db.Integer)
    bank_name = db.Column(db.String(12))
    branch = db.Column(db.String(24))
    tax_id = db.Column(db.Integer)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    about_me = db.Column(db.Text)
    active = db.Column(db.Boolean, default=True)
    confirmed = db.Column(db.Boolean, default=False)
    confirmed_at = db.Column(db.DateTime())
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime(), nullable=False)
    updated_at = db.Column(db.DateTime(), nullable=False)
    roles = db.relationship(
        "Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic")
    )
    sales = db.relationship('Sales', backref='user', lazy=True)

    def __repr__(self):
        return "<Name {}, Username {}, Role {}>".format(self.name, self.username, self.roles)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.roles == []:
            if self.email == current_app.config["MAIL_DEVELOPER"]:
                self.roles = [Role.query.filter_by(name="Developer").first()]
            if self.email == current_app.config["MAIL_ADMINISTRATOR"]:
                self.roles = [Role.query.filter_by(name="Admin").first()]
            if self.roles == []:
                self.roles = [Role.query.filter_by(name="Cashier").first()]

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return "https://www.gravatar.com/avatar/{}?id=identicon&s={}".format(
            digest, size
        )

    def get_id(self):
        return self.id

    def get_reset_password_token(self, expires_in=660):
        return jwt.encode(
            {"reset_password": self.id, "exp": time() + expires_in},
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        ).decode("utf-8")

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )["reset_password"]
        except:
            return
        return User.query.get(id)

    def create(self):
        """
        Create data from self and commit.
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Update user.
        """
        db.session.commit()

    @staticmethod
    def get(param):
        """
        Get user by username.
        @param is user username.
        """
        return User.query.filter_by(username=param).first()

    @staticmethod
    def get_by_email(param):
        """
        Get user by username.
        @param is user username.
        """
        return User.query.filter_by(email=param).first()

    @staticmethod
    def gets():
        """
        Get All User Data.
        """
        return User.query.all()

    @staticmethod
    def gets_for_user():
        """
        Get All User Data.
        """
        users = User.query.all()
        user = (user for user in users if user.roles != ["Developer"])
        return user

    @staticmethod
    def delete(param):
        """
        Delete user by username.
        @param is username of user
        """
        data = User.query.filter_by(username=param.lower()).first_or_404()
        db.session.delete(data)
        db.session.commit()

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps({"confirm": self.id}).decode("utf-8")

    def confirm(self, token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode("utf-8"))
        except:
            return False
        if data.get("confirm") != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True


class AnonymousUser(AnonymousUserMixin):
    pass


login.anonymous_user = AnonymousUser
