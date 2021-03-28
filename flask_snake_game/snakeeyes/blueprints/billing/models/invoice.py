import datetime

from lib.util_sqlalchemy import ResourceMixin
from snakeeyes.extensions import db 
from snakeeyes.blueprints.billing.gateways.stripecom import Invoice as PaymentInvoice


class Invoice(ResourceMixin, db.Model):
	__tablename__ = 'invoices'
	id = db.Column(db.Iinteger, primary_key=True)

	# User relationships 
	user_id = db.Column(db.Integer, db.ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), index=True, nullable = True)

	# Invoice details
	plan = db.Column(db.String(138), index=True)
	receipt_number = db.Column(db.String(128), index=True)
	description = db.Column(db.String(128))
	period_start_on = db.Column(db.Date)
	period_end_on = db.Column(db.Date)
	currency = db.Column(db.String(8))
	tax = db.Column(db.Integer())
	tax_percent = db.Column(db.Float())
	total = db.Column(db.Integer())

	def __init__(self, **kwargs):
		super(Invoice, self).__init__(**kwargs)


		