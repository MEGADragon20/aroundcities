from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from .config import Config
import stripe, logging

db = SQLAlchemy()
login_manager = LoginManager()



def create_app():
    app = Flask(__name__, static_url_path="/static", static_folder="/static")
    
    app.logger.setLevel(logging.DEBUG)
    app.logger.debug("App is beeing created")


    app.config.from_object(Config)
    print("Database URL:", app.config["SQLALCHEMY_DATABASE_URI"])


    stripe.api_key = app.config["STRIPE_SECRET_KEY"]

    db.init_app(app)
    #Migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = "main.login"

    from .routes import main
    app.register_blueprint(main)

    return app, db

@login_manager.user_loader
def load_user(user_id):
    from .models import User 
    return User.query.get(int(user_id))