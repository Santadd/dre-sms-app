from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, TextAreaField, 
                     SubmitField, EmailField, HiddenField)
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError
from app.models import User

#Create Student Admission Form
class StudentAdmissionForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    mid_name = StringField('Middle Name')
    email = StringField('Email', validators=[Email(), InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    reg_date = StringField('Registration Date')
    course = StringField('Course', validators=[InputRequired()])
    mobile_no = StringField('Mobile Number')
    admission_no = StringField('Admission Number', validators=[InputRequired()])
    birth_date = StringField('Birth Date', validators=[InputRequired()])
    student_id = StringField('Student ID', validators=[InputRequired()])
    student_class = StringField('Class', validators=[InputRequired()])
    department = StringField('Department', validators=[InputRequired()])
    religion = StringField('Religion')
    nationality = StringField('Nationality')
    father_name = StringField('Father\'s Name')
    mother_name = StringField('Mother\'s Name')
    father_occ = StringField('Father\'s Occupation')
    mother_occ = StringField('Mother\'s Occupation')
    father_email = EmailField('Father\'s Email')
    mother_email = EmailField('Mother\'s Email')
    father_mobile_no = StringField('Father\'s Mobile Number')
    mother_mobile_no = StringField('Mother\'s Mobile Number')
    present_add = TextAreaField('Present Address')
    permanent_add = TextAreaField('Permanent Address')
    
    submit = SubmitField('Submit')
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')
        
#Edit Student Details Form
class EditStudentForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    mid_name = StringField('Middle Name')
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password')
    reg_date = StringField('Registration Date')
    course = StringField('Course')
    mobile_no = StringField('Mobile Number')
    admission_no = StringField('Admission Number')
    birth_date = StringField('Birth Date')
    student_id = StringField('Student ID')
    student_class = StringField('Class')
    department = StringField('Department')
    religion = StringField('Religion')
    nationality = StringField('Nationality')
    father_name = StringField('Father\'s Name')
    mother_name = StringField('Mother\'s Name')
    father_occ = StringField('Father\'s Occupation')
    mother_occ = StringField('Mother\'s Occupation')
    father_email = EmailField('Father\'s Email')
    mother_email = EmailField('Mother\'s Email')
    father_mobile_no = StringField('Father\'s Mobile Number')
    mother_mobile_no = StringField('Mother\'s Mobile Number')
    present_add = TextAreaField('Present Address')
    permanent_add = TextAreaField('Permanent Address')
    
    submit = SubmitField('Submit')
    
    #Check for existing emails
    #def validate_email(self, email):
     #   if email.data != self.email and \
     #       User.query.filter_by(email=email.data).first():
      #      raise ValidationError('Email already in use. Use a different one.')
        
#Create Teacher Admission Form
class TeacherAdmissionForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    mid_name = StringField('Middle Name')
    email = StringField('Email', validators=[Email(), InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    join_date = StringField('Joining Date')
    course = StringField('Course', validators=[InputRequired()])
    mobile_no = StringField('Mobile Number')
    birth_date = StringField('Birth Date', validators=[InputRequired()])
    teacher_id = StringField('Teacher ID', validators=[InputRequired()])
    department = StringField('Department', validators=[InputRequired()])
    nationality = StringField('Nationality')
    permanent_add = TextAreaField('Permanent Address')
    account_type = HiddenField(default="Teacher Account")
    
    submit = SubmitField('Submit')
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')
        
        
#Edit Teacher Details Form
class EditTeacherForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    mid_name = StringField('Middle Name')
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password')
    join_date = StringField('Joining Date')
    course = StringField('Course')
    mobile_no = StringField('Mobile Number')
    birth_date = StringField('Birth Date')
    teacher_id = StringField('Teacher ID')
    department = StringField('Department')
    nationality = StringField('Nationality')
    permanent_add = TextAreaField('Permanent Address')
    
    submit = SubmitField('Submit')
    
    #def validate_email(self, field):
    #    if User.query.filter_by(email=field.data.lower()).first():
    #        raise ValidationError('Email already registered.')

#Register User    
class UserRegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    mid_name = StringField('Middle Name')
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[Email(), InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[InputRequired(), Length(min=8), 
                                    EqualTo('password', message="Passwords must match")])
    
    submit = SubmitField('Register')
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
        
#Edit User    
class EditUserForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    mid_name = StringField('Middle Name')
    username = StringField('Username')
    email = StringField('Email', validators=[Email(), InputRequired()])
    password = PasswordField('Password')
    submit = SubmitField('Update')
    
    """def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')
"""
    """def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')"""