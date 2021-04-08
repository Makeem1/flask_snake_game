from collections import OrderedDict

from flask_wtf import Form
from wtforms import (StringField, SelectField, BooleanField,
                    IntegerField, FloatField, SelectField, DateTimeField)
from wtforms.validators import DataRequired, Length, Regexp, Optional, NumberRange
from wtforms_components import Unique
from lib.utils_wtforms import ModelForm, choices_from_dict

from snakeeyes.blueprints.user.models import db, User
from snakeeyes.blueprints.billing.models.coupon import Coupon


class SearchForm(Form):
	search = StringField('Search terms', validators=[Optional(), Length(min=4, max=128, message='Limit your search text.')])
	

class BulkDeleteForm(Form):
    SCOPE = OrderedDict([
        ('all_selected_items', 'All selected items'),
        ('all_search_results', 'All search results')
    ])

    scope = SelectField('Privileges', [DataRequired()],
                        choices=choices_from_dict(SCOPE, prepend_blank=False))


class UserForm(ModelForm):
    username_message = 'Letters, numbers and underscores only please.'

    username = StringField(validators=[
        Unique(
            User.username,
            get_session=lambda: db.session
        ),
        Optional(),
        Length(1, 16),
        # Part of the Python 3.7.x update included updating flake8 which means
        # we need to explicitly define our regex pattern with r'xxx'.
        Regexp(r'^\w+$', message=username_message)
    ])

    role = SelectField('Privileges', [DataRequired()],
                       choices=choices_from_dict(User.ROLE,
                                                 prepend_blank=False))
    active = BooleanField('Yes, allow this user to sign in')

class UserCancelSubscriptionForm(Form):
    pass

class CouponForm(Form):
    percent_off = IntegerField('Percent of (%)',
                                validators=[Optional(), NumberRange(min=1, max=100)])
    amount_off = FloatField('Amount off ($)', 
                                validators=[Optional(), NumberRange(min=0.01, max=21474836.0)]
    currency = StringField('Code', 
                            validators=[DataRequired(), Length(min=1, max=32)])
    duration = SelectField('Duaration', 
                            validators=[DataRequired()], choices=choices_from_dict(Coupon.DURATION, prepend_blank=False))
    duration_in_months = IntegerField('Duration', 
                        validators=[Optional, NumberRange(min=1, max=12) ])
    max_redeemptions = IntegerField('Max Redeemptions', 
                                    validators=[Optional(), NumberRange(min=1, max=2147483647)])
    redeem_by = DateTimeField('Redeem by', 
                                validators=[Optional()], format='%Y-%m-%d %H:%M%S')

