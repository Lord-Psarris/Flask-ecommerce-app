from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# database
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'figaro_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    from .views import views
    from .auth import auth
    from .forms import forms

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth/')
    app.register_blueprint(forms, url_prefix='/forms/')

    from .models import Users
    create_database(app)

    # to tell flask which login manager to use
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('main/' + DB_NAME):
        db.create_all(app=app)
        print('Created db')
