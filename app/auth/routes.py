from flask import redirect, url_for, render_template, request, flash
from app import db
from app.models import User
from app.auth import auth
from app.auth.utils.email import send_email
from flask_login import login_user, login_required, current_user, logout_user
from app.auth.forms import LoginForm, PasswordResetForm, PasswordResetRequestForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.admin_dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        #Query for user object
        user = User.query.filter_by(email=form.email.data).first()
        print(user.role.name)
        #If user is found and password is correct, log user in
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            #get the next query parameter
            next = request.args.get('next')
            #If next is not available, return to landing page
            if next is None or not next.startswith('/'):
                #Log user into the neccessary dashboard based on role name
                if user.role.name == "Administrator":
                    next = url_for('admin.admin_dashboard')
                elif user.role.name == "Student":
                    next = url_for('student.student_dashboard')
                elif user.role.name == "Teacher":
                    next = url_for('teacher.teacher_dashboard')
            return redirect(next)
        #If user details is not found, flash an error message 
        flash("Invalid email or password", "danger")   
    return render_template('auth/login.html', title='Login Page', form=form)


@login_required
@auth.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for('auth.login'))

"""When a user requests a password reset, an email with a reset token is sent to the
registered email address. The user then clicks the link in the email and, after the
token is verified, a form is presented where a new password can be entered."""

@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('admin.admin_dashboard'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, ' Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token)
        flash('An email with instructions to reset your password has been sent to you', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/forgot_password.html', form=form, title='Reset Password')

#Reset Password
@auth.route('/resets/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('admin.admin_dashboard'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Your password has been reset successfully.', 'success')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('admin.admin_dashboard'))
    return render_template('auth/reset_password.html', form=form, title='Reset Password')

    