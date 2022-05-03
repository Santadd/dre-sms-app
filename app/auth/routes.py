from flask import redirect, url_for, render_template, request, flash
from app.models import User
from app.auth import auth
from flask_login import login_user, login_required, current_user, logout_user
from app.auth.forms import LoginForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #Query for user object
        user = User.query.filter_by(email=form.email.data).first()
        #If user is found and password is correct, log user in
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            #get the next query parameter
            next = request.args.get('next')
            #If next is not available, return to landing page
            if next is None or not next.startswith('/'):
                next = url_for('admin.admin_dashboard')
            return redirect(next)
        #If user details is not found, flash an error message
        flash("Invalid email or password")
        
    return render_template('auth/login.html', title='Login Page', form=form)


@login_required
@auth.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('auth.login'))
    