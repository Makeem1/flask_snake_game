from flask_wtf import Form
from wtforms import StringField, HiddenField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Optional, ValidationError
from wtforms_components import EmailField, Email, Unique 
from lib.utils_wtforms import ModelForm
from snakeeyes.blueprints.user.models import User
from snakeeyes.extensions import db 





class LoginForm(Form):
    """Login form """
    next = HiddenField()
    identity = StringField("Username or email ", validators=[DataRequired(), Length(min=4, max=200, message="Your identity is either too long or too short")])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=200, message='Your identity is either too long or too short')])
    remember_me = BooleanField('Stay signed in')


class RegistrationForm(ModelForm):
    email = EmailField(validators=[DataRequired(), Email(), Unique(User.email,get_session=lambda: db.session), Length(6, 128, message='Your email must be between 8-128 character')])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(8, 128), EqualTo('password', message="Input must match password field ")])


class WelcomeForm(ModelForm):
    username = StringField("Choose a username", validators=[DataRequired(), Unique(User.username, get_session=lambda:db.session), Length(min=4, max=16, message="Username must be more than four cahracter and less than 16 character")] )


class UpdateCredential(ModelForm):
    email = EmailField(validators=[Optional(), Email(), 
                Unique(User.email,get_session=lambda: db.session), Length(6, 128, message='Your email must be between 8-128 character')])
    new_password = PasswordField('New Password', validators=[Optional(), Length(8, 128)])
    confirm_password = PasswordField('Current Password', validators=[Optional(), Length(8, 128), EqualTo('new_password', message='Input must match new password field')])

class BeginPasswordResetForm(Form):
    email = EmailField('Email', validators=[DataRequired(), Length(6, 128, message='Your email must be between 8-128 character')])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There is not user with this email, you have to register first.")


class SettingNewPassword(Form):
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    confirm_password = PasswordField('Password', validators=[DataRequired(), Length(8, 128), EqualTo('password', message="Input must match password field ")])
    











                            