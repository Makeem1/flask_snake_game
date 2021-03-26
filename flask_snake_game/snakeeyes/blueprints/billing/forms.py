from flask_wtf import Form
from wtforms import HiddenField, StringField
from wtforms.validators import DataRequired, Optional, Length


class CreditCardForm(Form):
	stripe_key=HiddenField('Stripe Publishable key', validators=[DataRequired(), Length(1, 254)])
	plan = HiddenField('Plan', validators=[DataRequired(), Length(1, 254)])
	name = StringField('Name on card', validators=[DataRequired(), Length(1, 254)])
	coupon = StringField('Do you have a coupon?', validators=[Optional(), Length(1, 128)])

class UpdateSubscriptionForm(Form):
	coupon_code = StringField('Do you have a coupon code?', validators=[Optional(), Length(1, 125)])
	
class CancelSubscriptionForm(Form):
	pass