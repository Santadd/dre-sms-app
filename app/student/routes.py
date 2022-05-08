from flask import redirect, url_for, flash, render_template, request
from app.student import student
from flask_login import current_user, login_required
from app import db
from app.models import Student, Department


#Student Homepage
@student.route('/student_dashboard')
@login_required
def student_dashboard():
    no_of_departments = Department.query.count()
    students_in_class = Student.query.filter_by(studentclass_id = current_user.studentclass_id).count()
    return render_template('student/student_dashboard.html', title='My Dashboard', 
                           no_of_departments=no_of_departments, students_in_class=students_in_class)


#Students Profile page
@student.route('/profile_page', methods=['GET', 'POST'])
@login_required
def profile_page():
    #If student update his details
    if request.method == "POST":
        if request.form.get('password'):
            current_user.password = request.form.get('password')
        current_user.about_me = request.form.get('about_me')
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash("Student details updated successfully", "success")
        return redirect(url_for('student.profile_page'))
    return render_template('student/profile_page.html', title='Profile Page')

#View course
@student.route('/my_course')
@login_required
def my_course():
    return render_template('student/my_course.html', title='My Courses Page')


#View events
@student.route('/events')
@login_required
def event_page():
    return render_template('student/events.html', title='Events Page')

#View deparments
@student.route('/all_departments')
@login_required
def view_departments():
    departments = Department.query.all()
    return render_template('student/view_departments.html', title='All Departments page',
                           departments=departments)

