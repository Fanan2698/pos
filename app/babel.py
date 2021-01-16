from flask import g, request, current_app
from app import babel


@babel.localeselector
def get_locale():
    user = getattr(g, "user", None)
    if user is not None:
        return user.locale
    return request.accept_languages.best_match(current_app.config["LANGUAGES"])


@babel.timezoneselector
def get_timezone():
    user = getattr(g, "user", None)
    if user is not None:
        return user.timezone
