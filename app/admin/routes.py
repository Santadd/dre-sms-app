from flask import redirect, render_template, url_for
from app.admin import admin

@admin.route('')
def admin_home():
    return "Homepage levels"