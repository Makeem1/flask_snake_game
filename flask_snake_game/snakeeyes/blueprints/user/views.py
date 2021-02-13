from flask import request, flash, render_template, Blueprint, redirect
from snakeeyes.blueprints.user.forms import LoginForm, RegistrationForm, WelcomeForm
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
        if user is not None and user.authenticated(form.password.data):
            flash(f('your are now logged in as {form.identity.data}', 'success'))
            if login_user(user, remember=form.remember_me.data) and user.is_active():
                user.tracking_activities(request.remote_addr) 
                next_page = request.form.get('next')
                if next_page:
                    return redirect(safe_url(next_page))
                else:
                    return redirect('user.settings')
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
    return redirect('login')


@user.route('/welcome')
@login_required
def welcome():
    if current_user.username:
        return redirect(url_for('user.settings'))
        flash("You already pick a username", 'warning')
        
    form = WelcomeForm()
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
  
        user.username = form.username.data
        user.save()
        flash("Sign up is complete. Enjoy our service", "success")
        return redirect(url_for('user.'))
    return render_template('user/welcome.html', form = form )




























