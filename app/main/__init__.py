from flask import Blueprint

#create main blueprint
main = Blueprint("main", __name__)

from app.main import routes