from functools import wraps
from flask import g, request, redirect, url_for
from flask_login import current_user


def confirmation(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if (
            current_user.is_authenticated
            and not current_user.confirmed
            and request.blueprint != "auth"
            and request.endpoint != "static"
        ):
            return redirect(url_for("mod_auth.unconfirmed"))
        return f(*args, **kwargs)

    return decorated_function
