import sentry_sdk
from flask import Flask, request, render_template, g
from sentry_sdk.integrations.flask import FlaskIntegration
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, _
from flask_debugtoolbar import DebugToolbarExtension
from flask_marshmallow import Marshmallow

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()
toolbar = DebugToolbarExtension()
ma = Marshmallow()

login.login_view = "mod_auth.login"
login.login_message = _("Please log in to access this page.")


def page_not_found(e):
    """
    wide custome error page, 404
    """
    return render_template('error/404.html'), 404

def internal_server_error(e):
    """
    wide custome error page,500
    """
    return render_template('error/500.html'), 500

def create_app(config_class=Config):
    """
    function for create initial app
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    with app.app_context():
        if db.engine.url.drivername == 'sqlite':
            migrate.init_app(app, db, render_as_batch=True)
        else:
            migrate.init_app(app, db)    
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    toolbar.init_app(app)
    ma.init_app(app)

    from app.mod_dashboard import bp as dashboard_bp

    app.register_blueprint(dashboard_bp)

    from app.mod_auth import bp as auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.mod_user import bp as user_bp

    app.register_blueprint(user_bp, url_prefix="/user")

    from app.mod_role import bp as role_bp

    app.register_blueprint(role_bp, url_prefix="/role")

    from app.mod_bussines_profile import bp as profile_bp

    app.register_blueprint(profile_bp, url_prefix="/bussines-profile")

    from app.mod_app_profile import bp as app_profile_bp

    app.register_blueprint(app_profile_bp, url_prefix="/application-profile")

    from app.mod_category import bp as app_category_bp

    app.register_blueprint(app_category_bp, url_prefix="/category")

    from app.mod_product import bp as app_product_bp

    app.register_blueprint(app_product_bp, url_prefix="/product")

    from app.mod_pos import bp as pos_bp

    app.register_blueprint(pos_bp, url_prefix="/pos")

    from app.apis import bp as api_bp

    app.register_blueprint(api_bp, url_prefix="/api/v1")

    if not app.debug and not app.testing:
        if app.config["MAIL_SERVER"]:
            auth = None
        if app.config["MAIL_USERNAME"] or app.config["MAIL_PASSWORD"]:
            auth = (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
        secure = None
        if app.config["MAIL_USE_TLS"]:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
            fromaddr="no-reply@" + app.config["MAIL_SERVER"],
            toaddrs=app.config["MAIL_DEVELOPER"],
            subject="System Failure on " + app.config["APP_NAME"],
            credentials=auth,
            secure=secure,
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    if not os.path.exists("logs"):
        os.mkdir("logs")

    file_handler = RotatingFileHandler(
        "logs/flask-base.log", maxBytes=10240, backupCount=10
    )
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        )
    )
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("System Startup...")

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)

    return app

from app.mod_user import models
from app.mod_role import models
from app.mod_bussines_profile import models
from app.mod_app_profile import models
from app.mod_category import models
from app.mod_product import models
from app.mod_pos import models

