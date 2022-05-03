from tokenize import String
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import Email, InputRequired, Length


#Create LoginForm Class
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(message="Email field cannot be empty"), Email()])
    password = PasswordField('Password', validators=[InputRequired(message="Please enter your password")])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Sign In')