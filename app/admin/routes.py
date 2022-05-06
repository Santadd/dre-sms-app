from flask import current_app, redirect, render_template, url_for, request, flash
from app import db
from flask_login import current_user, login_required
from app.admin import admin
from app.admin.forms import (StudentAdmissionForm, UserRegistrationForm, TeacherAdmissionForm,
                             EditTeacherForm, EditStudentForm, EditUserForm)
from app.admin.utils import save_student_image, save_teacher_image, save_user_image
from app.models import Student, User, Teacher
from app.auth.utils.email import send_email
from app.auth.utils.decorators import permission_required, admin_required
import os

@admin.route('/dashboard')
@login_required
@admin_required
def admin_dashboard():
    return render_template('admin/index.html', title='Main Dashboard') 


#Register Students
@admin.route('/add_student', methods=['GET', 'POST'])
@login_required
@admin_required
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
        #Get student image
        student_pic = request.files.get('student_pic')
        if student_pic:
            student_image = save_student_image(student_pic)
        else:
            student_image = 'default.jpg'
        
        #Create a student instance and add details to database
        student = Student(first_name=first_name, last_name=last_name, mid_name=mid_name, reg_date=reg_date,
                          course=course, email=email, password=password, mobile_no=mobile_no, gender=gender,
                          admission_no=admission_no, birth_date=birth_date, student_id=student_id, 
                          student_class=student_class, department=department, religion=religion,
                          nationality=nationality, father_name=father_name, mother_name=mother_name,
                          father_occ=father_occ, mother_occ=mother_occ, father_email=father_email,
                          mother_email=mother_email, father_mobile_no=father_mobile_no,
                          mother_mobile_no=mother_mobile_no, present_add=present_add, 
                          permanent_add=permanent_add, user_image=student_image)
        db.session.add(student)
        db.session.commit()
        flash("Student details has been successfully added.", "success")
        return redirect(url_for('admin.add_student'))
    return render_template('admin/add_student.html', title='Add Student Page', form=form)


#Register Teachers
@admin.route('/add_teacher', methods=['GET', 'POST'])
@login_required
@admin_required
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
        account_type = form.account_type.data
        gender = request.form.get('gender')
        #Get teacher's image
        teacher_pic = request.files.get('teacher_pic')
        if teacher_pic:
            teacher_image = save_teacher_image(teacher_pic)
        else:
            teacher_image = 'default.jpg'
        #Create a teacher instance and add details to database
        teacher = Teacher(first_name=first_name, last_name=last_name, mid_name=mid_name, join_date=join_date,
                          course=course, email=email, password=password, mobile_no=mobile_no, gender=gender,
                          birth_date=birth_date, teacher_id=teacher_id, department=department, 
                          nationality=nationality, permanent_add=permanent_add, 
                          user_image=teacher_image, account_type=account_type)
        db.session.add(teacher)
        db.session.commit()
        flash("Teacher has been registered successfully.", "success")
        return redirect(url_for('admin.add_teacher'))
    return render_template('admin/add_teacher.html', title='Add Teacher Page', form=form)

#Add Users
@admin.route('/register_user', methods=["GET", "POST"])
@login_required
@admin_required
def register_user():
    form = UserRegistrationForm()
    if form.validate_on_submit():
        #Add new user to database
        #Get user's image
        user_pic = request.files.get('user_pic')
        if user_pic:
            user_image = save_user_image(user_pic)
        else:
            user_image = 'default.jpg'
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, 
                    mid_name=form.mid_name.data, username=form.username.data, email=form.email.data,
                    password=form.password.data, user_image=user_image, account_type=form.account_type.data)
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
@login_required
@admin_required
def view_students():
    students = Student.query.all()
    return render_template('admin/view_students.html', title='All Students Page', students=students)

#View Students List for editing
@admin.route('/students_list')
@login_required
@admin_required
def students_list():
    students = Student.query.all()
    return render_template('admin/students_list.html', title='All Students Page', students=students)

#Edit Student Details
@admin.route('/edit_student/<student_id>', methods=['GET', 'POST'])
@login_required
@admin_required
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
        
        #If new image is submitted, replace old image with the new one
        if request.files.get('student_pic'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/assets/images/users_profile/" +student.user_image))
                student.user_image = save_student_image(request.files.get('student_pic'))
            except:
                student.user_image = save_student_image(request.files.get('student_pic'))
                
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

#Delete Students
@admin.route('/delete_student/<student_id>', methods=['POST'])
@login_required
@admin_required
def delete_student(student_id):
    student = Student.query.filter_by(student_id=student_id).first_or_404()
    #If Student is found, delete students and redirect to page
    if request.method == "POST":
        db.session.delete(student)
        db.session.commit()
        flash(f"{student.first_name} {student.last_name}'s records have been deleted successfully", "success")
        return redirect(url_for('admin.students_list'))
    flash("Deletion operation could not be completed", "warning")
    return redirect(url_for('admin.students_list'))



#View Teachers
@admin.route('/view_teachers')
@login_required
@admin_required
def view_teachers():
    teachers = Teacher.query.all()
    return render_template('admin/view_teachers.html', title='All Teachers Page', teachers=teachers)

#View Teachers list for editing
@admin.route('/teachers_list')
@login_required
@admin_required
def teachers_list():
    teachers = Teacher.query.all()
    return render_template('admin/teachers_list.html', title='All Teachers Page', teachers=teachers)


#Edit Teachers Details
@admin.route('/edit_teacher/<teacher_id>', methods=['GET', 'POST'])
@login_required
@admin_required
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
        #If new image is submitted, replace old image with the new one
        if request.files.get('teacher_pic'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/assets/images/users_profile/" +teacher.user_image))
                teacher.user_image = save_teacher_image(request.files.get('teacher_pic'))
            except:
                teacher.user_image = save_teacher_image(request.files.get('teacher_pic'))
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

#Delete Teachers
@admin.route('/delete_teacher/<teacher_id>', methods=['POST'])
@login_required
@admin_required
def delete_teacher(teacher_id):
    teacher = Teacher.query.filter_by(teacher_id=teacher_id).first_or_404()
    #If teacher is found, delete teachers and redirect to page
    if request.method == "POST":
        db.session.delete(teacher)
        db.session.commit()
        flash(f"{teacher.first_name} {teacher.last_name}'s records have been deleted successfully", "success")
        return redirect(url_for('admin.teachers_list'))
    flash("Deletion operation could not be completed", "warning")
    return redirect(url_for('admin.teachers_list'))

#View all users
@admin.route('/view_users')
@login_required
@admin_required
def view_users():
    users = User.query.all()
    return render_template('admin/view_users.html', title='All Users Page', users=users)

#Edit users details
@admin.route('/edit_user/<user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    form = EditUserForm()
    
    user = User.query.get_or_404(user_id)
    #Update user Details if form is submitted
    if form.validate_on_submit():
        #Update password if new password is sumbitted
        if form.password.data:
            user.password = form.password.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.mid_name = form.mid_name.data
        user.email = form.email.data
        user.username = form.username.data
        #If new image is submitted, replace old image with the new one
        if request.files.get('user_pic'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/assets/images/users_profile/" +user.user_image))
                user.user_image = save_user_image(request.files.get('user_pic'))
            except:
                user.user_image = save_user_image(request.files.get('user_pic'))
        #commit update to database
        db.session.commit()
        flash(f"{user.first_name}'s details have been updated successfully", "success")
        return redirect(url_for('admin.edit_user', user_id=user.id))
    #Populate fields with user's details
    form.first_name.data = user.first_name
    form.last_name.data = user.last_name
    form.mid_name.data = user.mid_name
    form.email.data = user.email
    form.username.data = user.username
    return render_template('admin/edit_user.html', title='Edit User Page', 
                           user=user, form=form)
    
#Delete users
@admin.route('/delete_user/<user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    #If user is found, delete users and redirect to page
    if request.method == "POST":
        #Prevent administrator from being deleted
        if user.role.name == "Administrator":
            flash('Deletion operation cannot be applied on Administator', "warning")
            return redirect(url_for('admin.view_users'))
        db.session.delete(user)
        db.session.commit()
        flash(f"{user.first_name} {user.last_name}'s records have been deleted successfully", "success")
        return redirect(url_for('admin.view_users'))
    flash("Deletion operation could not be completed", "warning")
    return redirect(url_for('admin.view_users'))

