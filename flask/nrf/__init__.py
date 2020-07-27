import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from config import Config


logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
logger = logging.getLogger(__name__)

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


# def create_app():
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['JSON_AS_ASCII'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app_settings = os.getenv('APP_SETTINGS')
    # app.config.from_object(app_settings)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from nrf.users.routes import users
    from nrf.posts.routes import posts
    from nrf.main.routes import main
    from nrf.errors.handlers import errors
    from nrf.manualcoding.routes import manualcoding
    from nrf.datacollect.routes import datacollect
    from nrf.visualize.routes import visualize
    from nrf.nyt.routes import nyt
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(manualcoding)
    app.register_blueprint(datacollect)
    app.register_blueprint(visualize)
    app.register_blueprint(nyt)

    return app
