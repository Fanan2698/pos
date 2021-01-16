from flask import render_template, flash
from . import bp
from flask_security import login_required, roles_accepted
from app.helpers import unique_filename, get_db_image
from ..decorators import confirmation
from .forms import CreateApplicationProfile
from .models import ApplicationProfile
from flask_babel import _

@bp.route("/<string:filename>", methods=["GET"])
@login_required
@confirmation
@roles_accepted("Developer")
def display_image_logo(filename):
    data = ApplicationProfile.get_image(filename)
    return get_db_image(data.application_profile_logo_data, data.application_profile_logo_name)

@bp.route("/", methods=["GET", "POST"])
@login_required
@confirmation
@roles_accepted("Developer")
def application_profile():
    """
    Create or update application profile
    """
    form = CreateApplicationProfile()
    data = ApplicationProfile.get()
    if data is None:
        if form.validate_on_submit():
            data = ApplicationProfile(
                    application_profile_name=form.name.data,
                    application_profile_meta_title=form.meta_title.data,
                    application_profile_meta_description=form.meta_description.data,
                    application_profile_meta_keywords=form.meta_keywords.data
                    )
            if form.logo.data is not None:
                data.application_profile_logo_name=unique_filename(form.logo.data)
                data.application_profile_logo_data=form.logo.data.read()
            data.create()
            flash(_("Data {} successfully created").format(data.application_profile_meta_title.title()), "info")
    else:
        if form.validate_on_submit():
            data.application_profile_name=form.name.data
            data.application_profile_meta_title=form.meta_title.data
            data.application_profile_meta_description=form.meta_description.data
            data.application_profile_meta_keywords=form.meta_keywords.data
            if form.logo.data is not None:
                data.application_profile_logo_name=unique_filename(form.logo.data)
                data.application_profile_logo_data=form.logo.data.read()
            data.update()
            flash(_("Data {} successfully updated").format(data.application_profile_meta_title.title()), "info")
 
        form.name.data = data.application_profile_name
        form.meta_title.data = data.application_profile_meta_title
        form.meta_description.data = data.application_profile_meta_description
        form.meta_keywords.data = data.application_profile_meta_keywords

    return render_template("profile.html", form=form, title=_("Application Profile"), data=data)
