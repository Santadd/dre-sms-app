from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Email, Length


#Create Student Admission Form
class StudentAdmissionForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired(), Length(min=3)])
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
    father_email = StringField('Father\'s Email', validators=[Email()])
    mother_email = StringField('Mother\'s Email', validators=[Email()])
    father_mobile_no = StringField('Father\'s Mobile Number')
    mother_mobile_no = StringField('Mother\'s Mobile Number')
    present_add = TextAreaField('Present Address')
    permanent_add = TextAreaField('Permanent Address')
    
    submit = SubmitField('Submit')