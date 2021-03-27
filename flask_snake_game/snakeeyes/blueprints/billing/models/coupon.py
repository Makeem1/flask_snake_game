import datetime 
import string 
from collections import OrderedDict
from random import choice 

import pytz
from sqlalchemy import or_, and_

from sqlalchemy.ext.hybrid import hybrid_property

from lib.util_sqlalchemy import ResourceMixin, AwareDateTime
from lib.money import cents_to_dollars, dollars_to_cents
from snakeeyes.extensions import db 
from snakeeyes.blueprints.billing.gateways.stripecom import Coupon as PaymemtCoupon


class Coupon(ResourceMixin, db.Model):
	DURATION = OrderedDict([
			('forever', 'FOREVER'),
			('one', 'Once'),
			('repeating', 'Repeating')
		])

	__tablename__ = 'coupons'
	id = db.Column(db.Integer, primary_key=True)

	# Coupon details
	code = db.Column(db.String(128), index=True, unique=True)
	duration = db.Column(db.Enum(*DURATION, name='duration_types'), index=True, nullable=False, server_default='forever')

	amount_off = db.Column(db.Integer())
	percent_off = db.Column(db.Integer())
	currency = db.Column(db.String(8))
	durations_in_month = db.Column(db.Integer())
	max_redemptions = db.Column(db.Integer(), index=True)
	redeem_by = db.Column(AwareDateTime(), index=True)
	times_redeemed = db.Column(db.Integer(), index=True, nullable=False, default=0)
	valid = db.Column(db.Boolean(), nullable=False, server_default='1')

	def __init__(self, **kwargs):
		if self.code:
			self.code = self.code.upper()
		else:
			self.code = Coupon.random_coupon_code()


		super(Coupon, self).__init__(**kwargs)

