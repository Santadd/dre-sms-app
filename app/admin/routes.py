from flask import redirect, render_template, url_for, request, flash
from app import db
from flask_login import current_user, login_required
from app.admin import admin
from app.admin.forms import (StudentAdmissionForm, UserRegistrationForm, TeacherAdmissionForm,
                             EditTeacherForm, EditStudentForm)
from app.models import Student, User, Teacher
from app.auth.utils.email import send_email
from app.auth.utils.decorators import permission_required, admin_required

@admin.route('/dashboard')
@login_required
@admin_required
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


#Register Teachers
@admin.route('/add_teacher', methods=['GET', 'POST'])
@login_required
def add_teacher():
    form = TeacherAdmissionForm()
    if form.validate_on_submit():
        #Obtain teachers details
        first_name = form.first_name.data
        email = form.email.data
        last_name = form.last_name.data
        mid_name = form.mid_name.data
        join_date = form.join_date.data
        course = form.course.data
        password = form.password.data
        mobile_no = form.mobile_no.data
        birth_date = form.birth_date.data
        teacher_id = form.teacher_id.data
        department = form.department.data
        nationality = form.nationality.data
        permanent_add = form.permanent_add.data
        gender = request.form.get('gender')
        #Create a teacher instance and add details to database
        teacher = Teacher(first_name=first_name, last_name=last_name, mid_name=mid_name, join_date=join_date,
                          course=course, email=email, password=password, mobile_no=mobile_no, gender=gender,
                          birth_date=birth_date, teacher_id=teacher_id, department=department, 
                          nationality=nationality, permanent_add=permanent_add)
        db.session.add(teacher)
        db.session.commit()
        flash("Teacher has been registered successfully.", "success")
        return redirect(url_for('admin.add_teacher'))
    return render_template('admin/add_teacher.html', title='Add Teacher Page', form=form)

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


#View Students
@admin.route('/view_students')
def view_students():
    students = Student.query.all()
    return render_template('admin/view_students.html', title='All Students Page', students=students)

#View Students List for editing
@admin.route('/students_list')
def students_list():
    students = Student.query.all()
    return render_template('admin/students_list.html', title='All Students Page', students=students)

#Edit Student Details
@admin.route('/edit_student/<student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    form = EditStudentForm()
    
    student = Student.query.filter_by(student_id=student_id).first_or_404()
    #Update Student Details if form is submitted
    if form.validate_on_submit():
        #Update password if new password is sumbitted
        if form.password.data:
            student.password = form.password.data
        student.first_name = form.first_name.data
        student.last_name = form.last_name.data
        student.mid_name = form.mid_name.data
        student.email = form.email.data
        student.reg_date = form.reg_date.data
        student.course = form.course.data
        student.mobile_no = form.mobile_no.data
        student.nationality = form.nationality.data
        student.department = form.department.data
        student.birth_date = form.birth_date.data
        student.student_id = form.student_id.data
        student.permanent_add = form.permanent_add.data
        student.admission_no = form.admission_no.data
        student.student_class = form.student_class.data
        student.religion = form.religion.data
        student.father_name = form.father_name.data
        student.mother_name = form.mother_name.data
        student.father_email = form.father_email.data
        student.mother_email = form.mother_email.data
        student.father_occ = form.father_occ.data
        student.mother_occ = form.mother_occ.data
        student.father_mobile_no = form.father_mobile_no.data
        student.mother_mobile_no = form.mother_mobile_no.data
        student.present_add = form.present_add.data
        student.gender = request.form.get('gender')
        #commit update to database
        db.session.commit()
        flash(f"{student.first_name}'s details have been updated successfully", "success")
        return redirect(url_for('admin.edit_student', student_id=student.student_id))
    #Populate fields with Student's details
    form.first_name.data = student.first_name
    form.last_name.data = student.last_name
    form.mid_name.data = student.mid_name
    form.email.data = student.email
    form.reg_date.data = student.reg_date
    form.course.data = student.course
    form.mobile_no.data = student.mobile_no
    form.nationality.data = student.nationality
    form.department.data = student.department
    form.birth_date.data = student.birth_date
    form.student_id.data = student.student_id
    form.permanent_add.data = student.permanent_add
    form.admission_no.data = student.admission_no
    form.student_class.data = student.student_class
    form.religion.data = student.religion
    form.father_name.data = student.father_name
    form.mother_name.data = student.mother_name
    form.father_email.data = student.father_email
    form.mother_email.data = student.mother_email
    form.father_occ.data = student.father_occ
    form.mother_occ.data = student.mother_occ
    form.father_mobile_no.data = student.father_mobile_no
    form.mother_mobile_no.data = student.mother_mobile_no
    form.present_add.data = student.present_add
    return render_template('admin/edit_student.html', title='Edit Student Page', 
                           student=student, form=form)



#View Teachers
@admin.route('/view_teachers')
def view_teachers():
    teachers = Teacher.query.all()
    return render_template('admin/view_teachers.html', title='All Teachers Page', teachers=teachers)

#View Teachers list for editing
@admin.route('/teachers_list')
def teachers_list():
    teachers = Teacher.query.all()
    return render_template('admin/teachers_list.html', title='All Teachers Page', teachers=teachers)


#Edit Teachers Details
@admin.route('/edit_teacher/<teacher_id>', methods=['GET', 'POST'])
def edit_teacher(teacher_id):
    form = EditTeacherForm()
    
    teacher = Teacher.query.filter_by(teacher_id=teacher_id).first_or_404()
    #Update Teacher Details if form is submitted
    if form.validate_on_submit():
        #Update password if new password is sumbitted
        if form.password.data:
            teacher.password = form.password.data
        teacher.first_name = form.first_name.data
        teacher.last_name = form.last_name.data
        teacher.mid_name = form.mid_name.data
        teacher.email = form.email.data
        teacher.join_date = form.join_date.data
        teacher.course = form.course.data
        teacher.mobile_no = form.mobile_no.data
        teacher.nationality = form.nationality.data
        teacher.birth_date = form.birth_date.data
        teacher.teacher_id = form.teacher_id.data
        teacher.permanent_add = form.permanent_add.data
        teacher.department = form.department.data
        teacher.gender = request.form.get('gender')
        #commit update to database
        db.session.commit()
        flash(f"{teacher.first_name}'s details have been updated successfully", "success")
        return redirect(url_for('admin.edit_teacher', teacher_id=teacher.teacher_id))
    #Populate fields with teacher's details
    form.first_name.data = teacher.first_name
    form.last_name.data = teacher.last_name
    form.mid_name.data = teacher.mid_name
    form.email.data = teacher.email
    form.join_date.data = teacher.join_date
    form.course.data = teacher.course
    form.mobile_no.data = teacher.mobile_no
    form.nationality.data = teacher.nationality
    form.birth_date.data = teacher.birth_date
    form.teacher_id.data = teacher.teacher_id
    form.permanent_add.data = teacher.permanent_add
    form.department.data = teacher.department
    return render_template('admin/edit_teacher.html', title='Edit Teacher Page', 
                           teacher=teacher, form=form)
