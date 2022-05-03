from flask import redirect, render_template, url_for
from app.admin import admin

@admin.route('/dashboard')
def admin_dashboard():
    return render_template('admin/index.html', title='Main Dashboard') 

