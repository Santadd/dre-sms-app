from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


#Create instance of packages
mail = Mail()
db = SQLAlchemy()

#Create factory application for the app
def create_app(config_name):
    #Initialise the flask app
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    #Initialize the config object
    config[config_name].init_app()
    
    #Initialize all package instances
    db.init_app(app)
    mail.init_app(app)
    
    
    
    #Return application factory
    return app
    