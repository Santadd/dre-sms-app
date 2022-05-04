from flask import current_app
from app import db 
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from app import login_manager
import random
import string

#Define the user loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



"""Define Permission Class. Specify the type of permissions that can be performed"""
class Permission:
    READ = 1
    EDIT = 2
    MODERATE = 4
    ADMIN = 8
    
    

#Define Role Model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')
    
    #Set permissions filed to 0 if initial value isnt provided.
    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0
            
    """Define new methods to manage permissions. This is dependent on the permission constants"""
    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm
    
    #Create a static method that add roles to the Role class.
    @staticmethod
    def insert_roles():
        roles = {
            'Student': [Permission.READ, Permission.EDIT],
            'Teacher': [Permission.READ, Permission.EDIT, Permission.MODERATE],
            'Administrator': [Permission.READ, Permission.EDIT,
                              Permission.MODERATE, Permission.ADMIN],
        }
        default_role = 'Student'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit() 
            
    def __repr__(self):
        return '<Role %r>' % self.name
    
    


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    mid_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(50))
    username = db.Column(db.String(80), nullable=False, 
                         default=''.join(random.sample(string.ascii_lowercase, k=10)))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    email = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(120))
    confirmed = db.Column(db.Boolean, default=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'users',
        'with_polymorphic': '*',
        "polymorphic_on": type
    }
    
    """Define a default role upon registration, only exception is administrator
        whose role is assigned from the start.
    """
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['SMS_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
    
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
    
    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True
    
    """ Define a helper method to check whether users have a given 
        permission in the role the have been assigned
    """
    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)
    
    def __repr__(self):
        return "<User %r>" %self.username
 
#Anonymous User class that implements the can() and is_administrator() methods   
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

#Create Student Model
class Student(User):  
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    reg_date = db.Column(db.String(80))
    course = db.Column(db.String(80))
    mobile_no = db.Column(db.String(80))
    gender = db.Column(db.String(80))
    admission_no = db.Column(db.String(80))
    birth_date = db.Column(db.String(80))
    student_id = db.Column(db.String(80), index=True)
    student_class = db.Column(db.String(80))
    department = db.Column(db.String(80))
    religion = db.Column(db.String(80))
    nationality = db.Column(db.String(80))
    father_name = db.Column(db.String(80))
    mother_name = db.Column(db.String(80))
    father_occ = db.Column(db.String(80))
    mother_occ = db.Column(db.String(80))
    father_email = db.Column(db.String(80))
    mother_email = db.Column(db.String(80))
    father_mobile_no = db.Column(db.String(80))
    mother_mobile_no = db.Column(db.String(80))
    present_add = db.Column(db.Text)
    permanent_add = db.Column(db.Text)

    __mapper_args__ = {
        'polymorphic_identity': 'student',
        'with_polymorphic': '*'
    }
    
    
    def __repr__(self):
        return "<Student %r>" %self.student_id