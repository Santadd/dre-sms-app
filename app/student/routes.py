from flask import redirect, url_for, flash, render_template
from app.student import student
from flask_login import current_user, login_required
from app import db


#Student Homepage
@student.route('/student_dashboard')
def student_dashboard():
    return render_template('student/student_dashboard.html', title='My Dashboard')