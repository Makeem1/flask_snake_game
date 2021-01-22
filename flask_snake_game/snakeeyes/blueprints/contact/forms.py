from flask_wtf import Form
from wtforms import TextAreaField
from wtforms.validators import DataRequired, Length
from wtforms_components import EmailField 


class ContactForm(Form):
	email = EmailField(" What's your e-mail address?", validators=[DataRequired(), Length(min=4, max=254)])
	message = TextAreaField("What's is on your mind or issue ?", validators=[DataRequired(), Length(min=4, max=1875)])