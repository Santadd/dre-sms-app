from flask import redirect, render_template, url_for, flash, request
from app import db
from flask_login import login_required, current_user
from app.teacher import teacher
from app.models import Department, Teacher

#Teacher's Homepage
@teacher.route('/teacher_dashboard')
@login_required
def teacher_dashboard():
    no_of_departments = Department.query.count()
    no_of_teachers = Teacher.query.count()
    return render_template('teacher/teacher_dashboard.html', title='My Dashboard',
                           no_of_departments=no_of_departments, no_of_teachers=no_of_teachers)

#Teachers Profile page
@teacher.route('/profile_page', methods=['GET', 'POST'])
@login_required
def profile_page():
    #If teacher update his details
    if request.method == "POST":
        if request.form.get('password'):
            current_user.password = request.form.get('password')
        current_user.about_me = request.form.get('about_me')
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash("Teacher details updated successfully", "success")
        return redirect(url_for('teacher.profile_page'))
    return render_template('teacher/profile_page.html', title='Profile Page')

#View deparments
@teacher.route('/all_departments')
@login_required
def view_departments():
    departments = Department.query.all()
    return render_template('teacher/view_departments.html', title='All Departments page',
                           departments=departments)
    
#View events
@teacher.route('/events')
@login_required
def event_page():
    return render_template('teacher/events.html', title='Events Page')
