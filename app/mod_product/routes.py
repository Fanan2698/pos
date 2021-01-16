import os
from . import bp
from flask import render_template, redirect, flash, url_for, current_app, send_from_directory
from app.decorators import confirmation
from flask_security import roles_accepted, login_required
from .forms import CreateProduct, UpdateProduct
from flask_babel import _
from .models import Product
from datetime import datetime
from ..helpers import str2bool, unique_filename, get_local_image

#@bp.route("/<string:filename>", methods=["GET"])
#@login_required
#@confirmation
#@roles_accepted("Developer")
#def display_image(filename):
#    return send_from_directory('img/upload', filename)
    #return get_local_image(filename)


@bp.route('/', methods=['GET'])
@login_required
@roles_accepted("Developer", "Admin")
@confirmation
def products():
    products = Product.gets()
    return render_template('main/products.html', products=products, title=_("Products"))


@bp.route('/create', methods=['GET', 'POST'])
@login_required
@roles_accepted("Developer", "Admin")
@confirmation
def create_product():
    form = CreateProduct()
    if form.validate_on_submit():
        data = Product(product_name=form.name.data, product_price=form.price.data, product_stock=form.stock.data, category_id=form.category.data.id, created_at=datetime.now())
        if form.photo.data:
            # create unique filename and save it
            filename = unique_filename(form.photo.data)
            data.product_photo_filename = filename
            # set path to upload, save the file, save path
            if not os.path.exists(current_app.config['IMAGE_UPLOAD_DIR']):
                os.mkdir(current_app.config['IMAGE_UPLOAD_DIR'])
            else:
                path = os.path.join(current_app.config['IMAGE_UPLOAD_DIR'], filename)
                form.photo.data.save(path)
            # save path image without basedir, because it will call in direct from static folder
            data.product_photo_path = os.path.join(current_app.config['IMAGE_UPLOAD'], filename)
        data.create()
        flash(_("Data {} successfully created").format(data.product_name), "info")
        return redirect(url_for(".products"))
    return render_template('main/product.html', form=form, title=_('Create Data Products'))


@bp.route('/edit/<string:slug>', methods=["GET","POST"])
@login_required
@roles_accepted("Developer", "Admin")
@confirmation
def update_product(slug):
    data = Product.get(slug)
    form = UpdateProduct(data.product_name, category=data.category_id)
    if form.validate_on_submit():
        data.product_name = form.name.data
        data.product_price = form.price.data
        data.product_stock = form.stock.data
        data.category_id = form.category.data.id

        if form.photo.data:
            # create unique filename and save it
            filename = unique_filename(form.photo.data)
            data.product_photo_filename = filename
            # set path to upload, save the file, save path
            if not os.path.exists(current_app.config['IMAGE_UPLOAD_DIR']):
                os.mkdir(current_app.config['IMAGE_UPLOAD_DIR'])
            else:
                path_old_image = os.path.join(current_app.config["IMAGE_UPLOAD_DIR"], data.product_photo_filename)
                if os.path.exists(path_old_image):
                    os.remove(path_old_image)
                path = os.path.join(current_app.config['IMAGE_UPLOAD_DIR'], filename)
                form.photo.data.save(path)
            # save path image without basedir, because it will call in direct from static folder
            data.product_photo_path = os.path.join(current_app.config['IMAGE_UPLOAD'], filename)
        data.update()
        flash(_("Data {} sucessfully updated").format(data.product_name), "info")
        return redirect(url_for(".products"))
    form.name.data = data.product_name
    form.price.data = data.product_price
    form.stock.data = data.product_stock
    form.category.data = data.category_id
    return render_template('main/product.html', form=form, title=_("Update Data Products"))


@bp.route('/delete/<string:slug>')
@login_required
@roles_accepted("Developer", "Admin")
@confirmation
def delete_product(slug):
    data = Product.get(slug)
    path = os.path.join(current_app.config["IMAGE_UPLOAD_DIR"], data.product_photo_filename)
    if os.path.exists(path):
        os.remove(path)
    Product.delete(slug)
    flash(_("Data successfully delete"), "info")
    return redirect(url_for(".products"))


@bp.route('/activate/<string:slug>/<string:value>', methods=['GET', 'POST'])
@login_required
@roles_accepted("Developer", "Admin")
@confirmation
def activate_product(value, slug):
    data = Product.get(slug)
    data.product_status = str2bool(value)
    data.update()
    flash(_("Data {} sucessfully update").format(data.product_name), "info")
    return redirect(url_for(".products"))
