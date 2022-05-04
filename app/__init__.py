from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager


#Create instance of packages
mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()
#Set the login view page
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'

#Create factory application for the app
def create_app(config_name):
    #Initialise the flask app
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    #Initialize the config object
    config[config_name].init_app(app)
    
    #Initialize all package instances
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    
    #Attach Blueprints
    from app.admin import admin as admin_blueprint
    from app.main import main as main_blueprint
    from app.auth import auth as auth_blueprint
    from app.errors import errors as error_blueprint
    
    
    #Register Blueprints
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(error_blueprint)
    
    #Return application factory
    return app
    