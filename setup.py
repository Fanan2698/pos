import click
import os
from flask_security import Security, SQLAlchemyUserDatastore
from app import create_app, db
from app.mod_user.models import User
from app.mod_role.models import Role
from app.mod_category.models import ProductCategory
from app.mod_product.models import Product
from app.mod_bussines_profile.models import BusinessProfile
from app.mod_app_profile.models import ApplicationProfile
from app.mod_pos.models import Sales, Items
from datetime import datetime


app = create_app()
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Role": Role, "ProductCategory": ProductCategory, "Product": Product, "BusinessProfile": BusinessProfile, "ApplicationProfile": ApplicationProfile, "Sales": Sales, "Items": Items}


"""@app.before_request
def default():
    bp = BusinessProfile.get()
    return """

@app.before_first_request
def seed_roles():
    """ Insert Default Roles data only if Role table is empty. """
    if not Role.check_if_exist():
        cashier = user_datastore.create_role(
            name="Cashier", updated_at=datetime.utcnow(), created_at=datetime.utcnow(),
        )
        admin = user_datastore.create_role(
            name="Admin", updated_at=datetime.utcnow(), created_at=datetime.utcnow(),
        )
        developer = user_datastore.create_role(
            name="Developer", updated_at=datetime.utcnow(), created_at=datetime.utcnow(),
        )

        db.session.commit()
        app.logger.info("Seed default role data Success!")


def drop():
    """ Drop database """
    db.session.remove()
    db.drop_all()


@app.cli.group()
def translate():
    """ Translation and localization commands. """
    pass


@translate.command()
@click.argument("lang")
def init(lang):
    """Initialize a new language."""
    if os.system("pybabel extract -F babel.cfg -k _l -o messages.pot ."):
        raise RuntimeError("extract command failed")
    if os.system("pybabel init -i messages.pot -d app/translations -l " + lang):
        raise RuntimeError("init command failed")
    os.remove("messages.pot")


@translate.command()
def update():
    """Update all languages."""
    if os.system("pybabel extract -F babel.cfg -k _l -o messages.pot ."):
        raise RuntimeError("extract command failed")
    if os.system("pybabel update -i messages.pot -d app/translations"):
        raise RuntimeError("update command failed")
    os.remove("messages.pot")


@translate.command()
def compile():
    """Compile all languages."""
    if os.system("pybabel compile -d app/translations"):
        raise RuntimeError("compile command failed")
