from flask import current_app
from app import db 
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login_manager

#Define the user loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    mid_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(120))
    confirmed = db.Column(db.Boolean, default=False)
    
    #Define property for password. Make it write-only to prevent original password from being read
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    #Verify password
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    #Generating Confirmation Tokens with itsdangerous
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')
    
    #Confirm Toke
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        #Load token
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        #Check if the id from token matches the loggen-in user
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True
    
    def __repr__(self):
        return "<Users %r>" %self.username