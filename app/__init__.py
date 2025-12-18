from flask import Flask
from dotenv import load_dotenv
import os
from .models import db
from flask_login import LoginManager

login_manager = LoginManager()

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    # routes
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app

from .models.user import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))