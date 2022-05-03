from flask import Blueprint

#Create Blueprint name
admin = Blueprint('admin', __name__)

from app.admin import routes