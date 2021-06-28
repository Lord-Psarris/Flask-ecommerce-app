from . import db
from flask_login import UserMixin


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), unique=True)
    phone = db.Column(db.Integer)
    cart = db.relationship('Cart')


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(150))
    color = db.Column(db.String(15))
    size = db.Column(db.String(4))
    product_price = db.Column(db.Integer)
    product_image = db.Column(db.String(20000000))
    in_cart = db.relationship('Cart')


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer)
    colors_available = db.Column(db.String(1024))
