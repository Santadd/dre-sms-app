from flask import redirect, url_for, render_template
from app.main import main

#Create home route 
@main.route('/')
@main.route('/home')
def homepage():
    return redirect(url_for('auth.login')) 
