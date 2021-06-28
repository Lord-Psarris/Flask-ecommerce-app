"""
This contains the views where that communicates with the client side forms and other requests from the user
"""

from flask import Blueprint, flash, request, flash, redirect, url_for, jsonify
from .models import Users, Products, Cart
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re
from .views import get_path_from_name

forms = Blueprint('forms', __name__)


@forms.route('/sign-up', methods=["POST"])
def sign_up():
    email = request.form.get('email')
    full_name = request.form.get('fullname')
    phone = request.form.get('phone')
    password1 = request.form.get('password')
    confirm_password = request.form.get('confirmpassword')

    regex = '\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b'

    # validation
    user = Users.query.filter_by(email=email).first()
    if user:
        flash('This email already exists', category='error')
    elif re.search(regex, email):
        flash('Email format invalid', category='error')
    elif len(full_name) < 2:
        flash('Name must be  greater than 3 characters', category='error')
    elif password1 != confirm_password:
        flash('Passwords don\'t match', category='error')
    elif len(password1) < 7:
        flash('Password is too short', category='error')
    elif len(phone) > 13:
        flash('Phone number too long', category='error')
    elif '+' in phone:
        phone.replace('+', '')
    else:
        new_user = Users(email=email, phone=int(phone), username=full_name,
                         password=generate_password_hash(password1, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        flash('Account created', category='success')
        return redirect(url_for('auth.login'))

    return redirect(url_for('auth.login'))


@forms.route('/sign-in', methods=["POST"])
def sign_in():
    email = request.form.get('email')
    password = request.form.get('password')
    checkbox = request.form.get('checkbox')

    user = Users.query.filter_by(
        email=email).first()  # gets all the users with this email, .first() since email is unique
    if user:
        if check_password_hash(user.password, password):
            flash('Logged in successfully', category='success')
            if checkbox == 'on':
                login_user(user, remember=True)
            else:
                login_user(user)
            return redirect(url_for('views.index'))
        else:
            flash('Incorrect password', category='error')
    else:
        flash('Email does not exist', category='error')

    return redirect(url_for('auth.login'))


@forms.route('/add/to/cart', methods=['POST'])
@login_required
def add_to_cart():
    product_id = request.form.get('text')

    product = Products.query.filter_by(id=product_id).first()
    if product:
        color = product.color
        user_id = current_user.id
        quantity = 1

        in_Cart = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
        if in_Cart:
            flash('Product already in cart', category='error')
            return {}

        new_cart = Cart(user_id=user_id, product_id=product_id, quantity=quantity, colors_available=color)
        db.session.add(new_cart)
        db.session.commit()

        flash('Product added to cart', category='success')

    return {}


@forms.route('/cart/quantity', methods=['POST'])
@login_required
def adjust_cart_quantity():
    plus = request.form.get('plus')
    minus = request.form.get('minus')
    user_id = current_user.id

    if minus:
        product_id = minus
        cart = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
        p = Products.query.filter_by(id=int(product_id)).first()
        quantity = cart.quantity
        if quantity > 1:
            quantity -= 1
            cart.quantity = quantity
            db.session.commit()
    elif plus:
        product_id = plus
        cart = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
        quantity = cart.quantity
        quantity += 1
        cart.quantity = quantity
        db.session.commit()

    return {}


@forms.route('/cart/remove', methods=['POST'])
@login_required
def remove_from_cart():
    product_id = request.form.get('remove')
    user_id = current_user.id

    cart = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
    if cart:
        db.session.delete(cart)
        db.session.commit()
        flash('Product has been removed', category='success')

    return {}


@forms.route('/search', methods=['POST'])
def search():
    text = request.form.get('text')
    items = []
    products = Products.query.all()
    for product in products:
        if text.lower() in product.product_name.lower():
            ids = product.id
            items.append(ids)

    return jsonify({'items': items})