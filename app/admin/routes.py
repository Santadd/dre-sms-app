from flask import redirect, render_template, url_for
from app.admin import admin
from app.admin.forms import StudentAdmissionForm

@admin.route('/dashboard')
def admin_dashboard():
    return render_template('admin/index.html', title='Main Dashboard') 


@admin.route('/add_student', methods=['GET', 'POST'])
def add_student():
    form = StudentAdmissionForm()
    if form.validate_on_submit():
        return "Hey there"
    return render_template('admin/add_student.html', title='Add Student Page', form=form)

