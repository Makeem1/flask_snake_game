from flask import request, flash, render_template, Blueprint, redirect, url_for
from snakeeyes.blueprints.user.forms import (LoginForm, RegistrationForm, WelcomeForm, 
                                                        UpdateCredential, BeginPasswordResetForm, SettingNewPassword)
from flask_login import login_user, logout_user, login_required, current_user
from snakeeyes.blueprints.user.decorators import anonymous_required
from snakeeyes.blueprints.user.models import User

from lib.safe_next_url import safe_url


user = Blueprint('user', __name__, template_folder='templates')

@user.route('/login', methods=['GET', 'POST'])
@anonymous_required()
def login():
    form = LoginForm(next=request.args.get('next'))
    if form.validate_on_submit():
        user = User.find_by_identity(form.identity.data)
        if user is not None and user.authenticated(password=form.password.data):
            flash(f'your are now logged in as {form.identity.data}', 'success')
            if login_user(user, remember=form.remember_me.data) and user.is_active():
                user.tracking_activities(request.remote_addr) 
                next_page = request.form.get('next')
                if next_page:
                    return redirect(safe_url(next_page))
                else:
                    return redirect(url_for('user.welcome'))
            else:
                flash('Your account has been disable, please contact the customer for further information', 'warning')
        elif user is None:
            flash("There is no account with this identity", 'warning')
        else:
            flash("Incorrect identity or password", 'warning')
    return render_template('user/login.html', form=form)


@user.route('/register', methods=['GET', 'POST'])
@anonymous_required()
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        user.password = User.encrypt_password(form.password.data)
        user.save()
        if login_user(user):
            flash("'Awesome', Thanks for signing up", 'success')
            return redirect(url_for('user.welcome'))

    return render_template('user/registration.html', form = form )


@user.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out", 'success')
    return redirect(url_for('user.login'))


@user.route('/welcome', methods=['GET', 'POST'])
@login_required
def welcome():
    if current_user.username:
        flash("You've choose a username after registering, operation already done.", 'info')
        return redirect(url_for('user.settings'))
    form = WelcomeForm()
    if form.validate_on_submit():  
        current_user.username = form.username.data
        current_user.save()
        flash("Sign up is complete. Enjoy our service", "success")
        return redirect(url_for('user.settings'))
    return render_template('user/welcome.html', form = form )

@user.route('/settings')
def settings():
    return render_template('user/settings.html')


@user.route('/update_credentials', methods=['GET', 'POST'])
@login_required
def update_credentials():
    form = UpdateCredential()
    if form.validate_on_submit():
        new_password = form.new_password.data
        new_email = form.email.data
        if new_password:
            current_user.password = User.encrypt_password(new_password)
            flash("Your password has been updated", 'success')
        elif new_email:
            current_user.email = new_email
            flash("Your email address has been updated", 'success')
        else:
            flash('Your credentials has been updated', 'success')
        current_user.save()
        return redirect(url_for('user.settings'))
    return render_template('user/update_credentials.html', form=form )


@user.route('/begin_password_reset', methods=['GET', 'POST'])
@anonymous_required()
def begin_password_reset():
    form = BeginPasswordResetForm()

    if form.validate_on_submit():
        u = User.initialize_password_reset(request.form.get('identity'))

        flash('An email has been sent to {0}.'.format(u.email), 'success')
        return redirect(url_for('user.login'))

    return render_template('user/begin_password_reset.html', form=form)



@user.route('/newpassword', methods=('GET', 'POST'))
@anonymous_required
def newpassword(token):

    form = SettingNewPassword(reset_token = request.args.get('reset_token'))
    if form.validate_on_submit():
        user = User.deserializer_token(request.form.get('reset_token'))
        if user is None:
            flash('Your reset token has expired or tampered with.', 'danger')
            return redirect(url_for('user.begin_password_reset'))


        form.populate_obj(user)
        user.password = User.encrypt_password(request.form.get('password'))
        user.save()

        if login_user(user):
            flash("Your paasword has been reset.", "Success")
            return redirect(url_for('user.settings'))
        return render_template('user/new_password.html', form = form )


























