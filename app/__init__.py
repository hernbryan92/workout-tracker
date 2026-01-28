from flask import Flask 
from flask_login import LoginManager
from .models import db, User
import os

login_manager = LoginManager()
login_manager.login_view = 'auth.login' # where to redirect if not logged in


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key'

    # stable sqlite path
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout_tracker.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)

    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes import main
    from .auth import auth 
    app.register_blueprint(main)
    app.register_blueprint(auth)

    with app.app_context():
        db.create_all()
    
    return app
    