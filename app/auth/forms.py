from flask_wtf import FlaskForm
from app.models import User
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import Email, InputRequired, Length, EqualTo, ValidationError


#Create LoginForm Class
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(message="Email field cannot be empty"), Email()])
    password = PasswordField('Password', validators=[InputRequired(message="Please enter your password")])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Sign In')
    
class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    submit = SubmitField('Reset Password')

    #Check if email exists
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('Email does not exist. Please check and try again')

class PasswordResetForm(FlaskForm):
    password = PasswordField('New Password', validators=[InputRequired(), Length(min=8),
                                            EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[InputRequired(), Length(min=8)])
    submit = SubmitField('Reset Password')