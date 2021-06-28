"""
This file handles the main views for the webserver, including
the index/products page and cart page
"""

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from .models import Products, Cart
from . import db
import glob
import random

views = Blueprint('views', __name__)


def get_path_from_name(name):
    files = glob.glob('main/assets/**/*.jpg', recursive=True)
    for file in files:
        if name in file:
            file = file.replace('main/', '')
            return file


@views.route('/')
def index():
    products_from_db = Products.query.all()
    product_to_template = []
    for product in products_from_db:
        path = product.product_name.replace('main/assets', '')

        try:
            in_Cart = Cart.query.filter_by(user_id=current_user.id, product_id=product.id).first()
            if in_Cart:
                in_cart = True
            else:
                in_cart = False
        except:
            in_cart = False

        products = {
            'name': product.product_name,
            'path': '../static/' + get_path_from_name(path),
            'price': product.product_price,
            'id': product.id,
            'in_cart': in_cart
        }
        product_to_template.append(products)

    return render_template("index.html", products=product_to_template)


@views.route('/cart')
@login_required
def cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    no_of_cart_items = len(cart_items)
    cart_to_template = []
    subtotal = 0

    for item in cart_items:
        product_id = item.product_id
        product = Products.query.filter_by(id=product_id).first()

        path = product.product_name.replace('main/assets', '')

        items_dict = {
            'id': product_id,
            'name': product.product_name,
            'image_path': '../static/' + get_path_from_name(path),
            'price': int(product.product_price) * int(item.quantity),
            'color': product.color,
            'size': product.size,
            'quantity': item.quantity
        }
        subtotal += items_dict['price']
        cart_to_template.append(items_dict)

    return render_template("cart.html", item_number=no_of_cart_items, items=cart_to_template, subtotal=subtotal)


# to add products to the database
# the images should be placed in the assets folder, and named appropriately
@views.route('/add/to/products/db')
def add():
    files = glob.glob('main/assets/**/*.jpg', recursive=True)
    random.seed(999)

    prices = [35, 22, 18, 20, 40, 10]
    colors = ['red', 'blue', 'white', 'white', 'black', 'grey']
    sizes = ['M', 'XL', 'L']

    for file in files:
        file_ = file.replace('main/assets\\', '')
        file_name = file_.split('.')[0]
        file_data = open(file, 'rb').read()
        price = random.choices(prices)[0]
        color = random.choices(colors)[0]
        size = random.choices(sizes)[0]

        files_ = Products.query.filter_by(product_name=file_name).first()
        if files_ is None:
            new_products = Products(product_name=file_name, product_price=price, product_image=file_data,
                                    color=color, size=size)
            db.session.add(new_products)
            db.session.commit()

    return redirect(url_for('views.index'))
