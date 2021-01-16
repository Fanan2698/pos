import os
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, ".env"))


class Config(object):
    """
    Configuration system
    """
    APP_NAME = os.getenv("APP_NAME") or "Default App"
    SECRET_KEY = os.getenv("SECRET_KEY") or "let-me-in-please"
    LOG_TO_STDOUT = os.getenv("LOG_TO_STDOUT") or "False"

    """Flask SQLAlchemy Configuration"""
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or "sqlite:///" + os.path.join(
        BASEDIR, "boilerplate_flask_pos.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    """Flask Mail Configuration"""
    MAIL_SERVER = os.getenv("MAIL_SERVER") or "localhost"
    MAIL_PORT = int(os.getenv("MAIL_PORT") or 8025)
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS") or False
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL") or False
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEVELOPER = os.getenv("MAIL_DEVELOPER")
    MAIL_ADMINISTRATOR = os.getenv("MAIL_ADMINISTRATOR")
    
    """Upload Folder"""
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
    STATIC_DIR =  os.path.join(os.path.dirname(os.path.realpath(__file__)), 'app/static')
    IMAGE_UPLOAD = 'img/upload'
    IMAGE_UPLOAD_DIR = os.path.join(STATIC_DIR, IMAGE_UPLOAD)
    
    """Flask Babel Configuration"""
    BABEL_DEFAULT_LOCALE = "id"
    BABEL_DEFAULT_TIMEZONE = "UTC+7"
    LANGUAGES = ["en", "id"]
    
    """Flask Security Configuration"""
    SECURITY_LOGIN_URL = "/auth/login"
    SECURITY_POST_LOGIN_VIEW = "/"
    SECURITY_REGISTERABLE = True
    SECURITY_REGISTER_URL = "/auth/register"
    SECURITY_POST_REGISTER_VIEW = "/auth/login"
    SECURITY_LOGOUT_URL = "/auth/logout"
    SECURITY_POST_LOGOUT_VIEW = "/auth/login"

    """Flask Debugtoolbar Configuration"""
    DEBUG_TB_INTERCEPT_REDIRECTS = False