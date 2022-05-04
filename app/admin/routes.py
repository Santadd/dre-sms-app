from flask import redirect, render_template, url_for, request, flash
from app import db
from flask_login import current_user, login_required
from app.admin import admin
from app.admin.forms import StudentAdmissionForm, UserRegistrationForm
from app.models import Student, User
from app.auth.utils.email import send_email

@admin.route('/dashboard')
@login_required
def admin_dashboard():
    return render_template('admin/index.html', title='Main Dashboard') 


#Register Students
@admin.route('/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    form = StudentAdmissionForm()
    if form.validate_on_submit():
        #Obtain students details
        first_name = form.first_name.data
        email = form.email.data
        last_name = form.last_name.data
        mid_name = form.mid_name.data
        reg_date = form.reg_date.data
        course = form.course.data
        password = form.password.data
        mobile_no = form.mobile_no.data
        admission_no = form.admission_no.data
        birth_date = form.birth_date.data
        student_id = form.student_id.data
        student_class = form.student_class.data
        department = form.department.data
        religion = form.religion.data
        nationality = form.nationality.data
        father_name = form.father_name.data
        mother_name = form.mother_name.data
        father_occ = form.father_occ.data
        mother_occ = form.mother_occ.data
        father_email = form.father_email.data
        mother_email = form.mother_email.data
        father_mobile_no = form.father_mobile_no.data
        mother_mobile_no = form.mother_mobile_no.data
        present_add = form.present_add.data
        permanent_add = form.permanent_add.data
        gender = request.form.get('gender')
        #Create a student instance and add details to database
        student = Student(first_name=first_name, last_name=last_name, mid_name=mid_name, reg_date=reg_date,
                          course=course, email=email, password=password, mobile_no=mobile_no, gender=gender,
                          admission_no=admission_no, birth_date=birth_date, student_id=student_id, 
                          student_class=student_class, department=department, religion=religion,
                          nationality=nationality, father_name=father_name, mother_name=mother_name,
                          father_occ=father_occ, mother_occ=mother_occ, father_email=father_email,
                          mother_email=mother_email, father_mobile_no=father_mobile_no,
                          mother_mobile_no=mother_mobile_no, present_add=present_add, 
                          permanent_add=permanent_add)
        db.session.add(student)
        db.session.commit()
        flash("Student details has been successfully added.", "success")
        return redirect(url_for('admin.add_student'))
    return render_template('admin/add_student.html', title='Add Student Page', form=form)

#Add Users
@admin.route('/register_user', methods=["GET", "POST"])
def register_user():
    form = UserRegistrationForm()
    if form.validate_on_submit():
        #Add new user to database
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, 
                    mid_name=form.mid_name.data, username=form.username.data, email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        #Generate user token
        token = user.generate_confirmation_token()
        #Send confirmation email to user
        send_email(user.email, ' Confirm Your Account',
                   'auth/email/user_confirm', user=user, token=token)
        flash("User account has been created successfully. \
                Account confirmation email has been via by email.", "success")
        return redirect(url_for('admin.register_user'))
    return render_template('admin/register_user.html', title='Register User', form=form)

#Confirm User Account
@admin.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('admin.admin_dashboard'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('admin.admin_dashboard'))