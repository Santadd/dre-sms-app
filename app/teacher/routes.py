from flask import redirect, render_template, url_for, flash
from app import db
from flask_login import login_required
from app.teacher import teacher

#Teacher's Homepage
@teacher.route('/teacher_dashboard')
def teacher_dashboard():
    return render_template('teacher/teacher_dashboard.html', title='My Dashboard')