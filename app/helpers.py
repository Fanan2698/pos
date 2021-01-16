import uuid, os
from io import BytesIO
from flask import send_file, current_app


def unique_filename(data):
    """
    Create unique and secure filename

    @data is field name of current data now.
    """
    file = data
    get_ext = file.filename.split(".")[-1]
    new_name = "%s.%s" % (uuid.uuid4().hex, get_ext)
    return new_name


def get_db_image(param1, param2):
    """
    Display image from database

    @param1 param1 is field data,
    @param2 param2 is field name of data
    """
    return send_file(
        BytesIO(param1),
        mimetype="images/generic",
        as_attachment=True,
        attachment_filename=param2,
    )


def allowed_file(filename):
    """
    Function that matching file upload extension with whitelist extension
    """
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


def unique_filename_for_user(data, username):
    """
    Create unique and secure filename

    @data is field name of current data now.
    @username is field username of selected data.
    """
    file = data
    get_ext = file.filename.split(".")[-1]
    new_name = "%s.%s" % (username, get_ext)
    return new_name


def delete_local_image(filename):
    """
    Delete image with @filename parameter
    """
    directory = os.listdir(current_app.config["UPLOAD_FOLDER"])
    filename = [image for image in directory if filename in image]
    os.remove(current_app.config["UPLOAD_FOLDER"] + filename[0])


def get_local_image(filename):
    """
    get image with @filename parameter
    """
    directory = os.listdir(current_app.config["IMAGE_UPLOAD_DIR"])
    filename = [image for image in directory if filename in image]
    return filename


def str2bool(v):
    """
    String To Boolean
    """
    return v.lower() in ("yes", "true", "t", "1", "True")
