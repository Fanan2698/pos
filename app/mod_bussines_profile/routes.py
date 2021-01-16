from flask import render_template, flash, current_app
from . import bp
from app import db
from app.helpers import unique_filename, get_db_image 
from .models import BusinessProfile
from .forms import CreateBusinessProfile
from flask_security import login_required, roles_accepted
from werkzeug.utils import secure_filename
from datetime import datetime
from flask_babel import _
from ..decorators import confirmation


@bp.route("/<string:filename>", methods=["GET"])
@login_required
@confirmation
def display_image_logo(filename):
    """
    function to load image from local path source
    """
    data = BusinessProfile.get_image(filename)
    return get_db_image(data.business_profile_logo, data.business_profile_logo_name)


@bp.route("/", methods=["GET", "POST"])
@login_required
@roles_accepted("Developer", "Admin")
@confirmation
def create_business_profile():
    """
    function that create or update business profile data on apps
    """
    form = CreateBusinessProfile()
    data = BusinessProfile.get()
    if data is None:
       if form.validate_on_submit():
            data = BusinessProfile(
                business_profile_name=form.name.data,
                business_profile_address=form.address.data,
                business_profile_sub_district=form.sub_district.data,
                business_profile_district=form.district.data,
                business_profile_province=form.province.data,
                business_profile_country=form.country.data,
                business_profile_postal_code=form.postal_code.data,
                business_profile_phone_number=form.phone_number.data,
                business_profile_email=form.email.data,
                business_profile_website=form.website.data,
                business_profile_created_at=datetime.utcnow(),
                business_profile_updated_at=datetime.utcnow(),
            )
            data.business_profile_social_media = {
                "twitter": form.twitter.data,
                "instagram": form.instagram.data,
                "youtube": form.youtube.data,
                "facebook": form.facebook.data,
            }
            if form.logo.data is not None:
                data.business_profile_logo = form.logo.data.read()
                data.business_profile_logo_name = unique_filename(form.logo.data)
            data.create()
            flash(
                _(
                   "Data {} successfully created").format(
                        data.business_profile_name.title()
                    )
                ,
                "info",
            )
    else:
        """
        If bussiness profile is exist and then update bussiness profile.
        """
        if form.validate_on_submit():
            data.business_profile_name = form.name.data
            data.business_profile_address = form.address.data
            data.business_profile_sub_district = form.sub_district.data
            data.business_profile_district = form.district.data
            data.business_profile_province = form.province.data
            data.business_profile_country = form.country.data
            data.business_profile_postal_code = form.postal_code.data
            data.business_profile_phone_number = form.phone_number.data
            data.business_profile_email = form.email.data
            data.business_profile_website = form.website.data
            data.business_profile_updated_at = datetime.utcnow()
            data.business_profile_social_media = {
                "twitter": form.twitter.data,
                "instagram": form.instagram.data,
                "youtube": form.youtube.data,
                "facebook": form.facebook.data,
            }
            if form.logo.data is not None:
                data.business_profile_logo = form.logo.data.read()
                data.business_profile_logo_name = unique_filename(form.logo.data)
            data.update()
            flash(
                _(
                    "Data {} successfully updated").format(
                        data.business_profile_name.title()
                    )
                ,
                "info",
            )
        form.name.data = data.business_profile_name
        form.address.data = data.business_profile_address
        form.sub_district.data = data.business_profile_sub_district
        form.district.data = data.business_profile_district
        form.province.data = data.business_profile_province
        form.country.data = data.business_profile_country
        form.postal_code.data = data.business_profile_postal_code
        form.phone_number.data = data.business_profile_phone_number
        form.email.data = data.business_profile_email
        form.website.data = data.business_profile_website
        form.instagram.data = data.business_profile_social_media["instagram"]
        form.facebook.data = data.business_profile_social_media["facebook"]
        form.twitter.data = data.business_profile_social_media["twitter"]
        form.youtube.data = data.business_profile_social_media["youtube"]
    return render_template(
        "profiles/profile.html", title=_("Business Profile"), form=form, data=data,
    )
