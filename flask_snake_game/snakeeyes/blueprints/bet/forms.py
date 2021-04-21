from flask_wtf import Form 
from wtforms import IntegerField
from wtforms.validators import DataRequired, NumberRange


class BetForm(Form):
	geuss = IntegerField('Guess', validators=[DataRequired(), NumberRange(min=1, max=12)])
	wagered = IntegerField('Wagered', validators=[DataRequired(), NumberRange(min=1)])