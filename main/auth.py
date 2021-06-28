"""
This contains all the views the user goes to for authentication
"""

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, logout_user

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template("login.html")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
