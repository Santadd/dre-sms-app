from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, TextAreaField, 
                     SubmitField, EmailField, HiddenField)
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError
from app.models import User, Course, Department, StudentClass, Teacher, Student
from flask_login import current_user

#Create Student Admission Form
class StudentAdmissionForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    mid_name = StringField('Middle Name')
    email = StringField('Email', validators=[Email(), InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    reg_date = StringField('Registration Date')
    mobile_no = StringField('Mobile Number')
    admission_no = StringField('Admission Number', validators=[InputRequired()])
    birth_date = StringField('Birth Date', validators=[InputRequired()])
    student_id = StringField('Student ID', validators=[InputRequired()])
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
        
    def validate_admission_no(self, field):
        if Student.query.filter_by(admission_no=field.data.lower()).first():
            raise ValidationError('A student already has this admission number. Use another one')
        
    def validate_student_id(self, field):
        if Student.query.filter_by(student_id=field.data.lower()).first():
            raise ValidationError('A sudent with this ID has been already registered. Try another one')
        
#Edit Student Details Form
class EditStudentForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    mid_name = StringField('Middle Name')
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password')
    reg_date = StringField('Registration Date')
    mobile_no = StringField('Mobile Number')
    admission_no = StringField('Admission Number')
    birth_date = StringField('Birth Date')
    student_id = StringField('Student ID')
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
    
    def __init__(self, user):
        super().__init__()
        self.user = user
    
    #Check for existing emails
    def validate_email(self, field):
        if field.data != self.user.email and \
            User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError(f'"{field.data}" already in use. Use a different one.')
        
    #Check for existing student ID 
    def validate_student_id(self, field):
        if field.data != self.user.student_id and \
            Student.query.filter_by(student_id=field.data.lower()).first():
            raise ValidationError(f'Student ID "{field.data}" already in use. Use a different one.')
        
    #Check for existing Admission Number ID 
    def validate_admission_no(self, field):
        if field.data != self.user.admission_no and \
            Student.query.filter_by(admission_no=field.data.lower()).first():
            raise ValidationError(f'Student Admission No. "{field.data}" is already taken. Use a different one.')
        
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
        
    def validate_teacher_id(self, field):
        if Teacher.query.filter_by(teacher_id=field.data.lower()).first():
            raise ValidationError('A teacher already has this ID. Try another one')
        
        
#Edit Teacher Details Form
class EditTeacherForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    mid_name = StringField('Middle Name')
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password')
    join_date = StringField('Joining Date')
    mobile_no = StringField('Mobile Number')
    birth_date = StringField('Birth Date')
    teacher_id = StringField('Teacher ID')
    nationality = StringField('Nationality')
    permanent_add = TextAreaField('Permanent Address')
    
    submit = SubmitField('Submit')
    
    def __init__(self, user):
        super().__init__()
        self.user = user
    
    #Check for existing emails
    def validate_email(self, field):
        if field.data!= self.user.email and User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError(f'"{field.data}" has been registered already. Use a different one')
        
    #Check for existing teacher id
    def validate_teacher_id(self, field):
        if field.data!= self.user.teacher_id and Teacher.query.filter_by(teacher_id=field.data.lower()).first():
            raise ValidationError(f'Teacher ID "{field.data}" is already taken. Use a different one')

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
    account_type = HiddenField(default="User Account")
    
    submit = SubmitField('Register')
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
        
#Edit User    
class UserEditForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    mid_name = StringField('Middle Name')
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[Email(), InputRequired()])
    password = PasswordField('Password')
    
    submit = SubmitField('Update')
    
    def validate_email(self, field):
        if field.data!= current_user.email and User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered. Use a different email')

    def validate_username(self, field):
        if field.data!= current_user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use. Try another one')
        
#Edit User    
class EditUserForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    mid_name = StringField('Middle Name')
    username = StringField('Username')
    email = StringField('Email', validators=[Email(), InputRequired()])
    password = PasswordField('Password')
    submit = SubmitField('Update')
    
    def __init__(self, user):
        super().__init__()
        self.user = user
    
    def validate_email(self, field):
        if field.data !=self.user.email and User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError(f'"{field.data}" already registered. Use a different email.')

    def validate_username(self, field):
        if field.data !=self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError(f'Username "{field.data}" already in use. Try another one.')
            
#Add Course form
class AddCourseForm(FlaskForm):
    coursename = StringField('Course Name', validators=[InputRequired(message="Please enter a course")])
    submit = SubmitField('Add Course')
    
    def validate_coursename(self, field):
        if Course.query.filter_by(name=field.data).first():
            raise ValidationError('Course name already exits.')
        
#Edit Course form
class EditCourseForm(FlaskForm):
    coursename = StringField('Course Name')
    submit = SubmitField('Edit Course')
    
    def __init__(self, coursename):
        super().__init__()
        self.course = coursename
    
    
    def validate_coursename(self, field):
        if field.data!= self.course.name and Course.query.filter_by(name=field.data).first():
            raise ValidationError(f'Course name "{field.data}" already exits. Use a different one')
    
#Add Deparment form
class AddDepartmentForm(FlaskForm):
    departmentname = StringField('Department Name', validators=[InputRequired(message="Please enter a Department")])
    submit = SubmitField('Add Department')
    
    
    def validate_departmentname(self, field):
        if Department.query.filter_by(name=field.data).first():
            raise ValidationError('Department name already exits.')
        
#Edit department form
class EditDepartmentForm(FlaskForm):
    departmentname = StringField('Department Name')
    submit = SubmitField('Edit Department')
    
    def __init__(self, departmentname):
        super().__init__()
        self.department = departmentname
    
    
    def validate_departmentname(self, field):
        if field.data!= self.department.name and Department.query.filter_by(name=field.data).first():
            raise ValidationError(f'Department name "{field.data}" already exits. Use a different one')
            
#Add Deparment form
class AddStudentClassForm(FlaskForm):
    studentclass = StringField('Class', validators=[InputRequired(message="Please enter a class")])
    submit = SubmitField('Add Class')
    
    
    def validate_studentclass(self, field):
        if StudentClass.query.filter_by(name=field.data).first():
            raise ValidationError('class already exits.')
        
#Edit studentclass form
class EditStudentClassForm(FlaskForm):
    studentclass = StringField('Class')
    submit = SubmitField('Edit class')
    
    def __init__(self, studentclass):
        super().__init__()
        self.stdclass = studentclass
    
    
    def validate_studentclass(self, field):
        if field.data!= self.stdclass.name and StudentClass.query.filter_by(name=field.data).first():
            raise ValidationError(f'Class "{field.data}" has been created already. Use a different one')


