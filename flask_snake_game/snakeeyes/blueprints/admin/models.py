from snakeeyes.blueprints.user.models import User
from snakeeyes.blueprints.billing.models.subscription import Subscription
from sqlalchemy import func
from snakeeyes.extensions import db 

class Dashboard(object):
	@classmethod
	def group_and_count_users(cls):
		"""Provide a group and count on all user"""
		return Dashboard._group_and_count(User, User.role)


	@classmethod
	def group_and_count_plans(cls):
		"""
		Provide a group by and count all subscribers
		"""
		return Dashboard._group_and_count(Subscription, Subscription.plan)

	@classmethod
	def group_and_count_coupons(cls):
		"""
		Obtain coupon usage statistics across all subscribers.

		:return: tuple
		"""
		not_null = db.session.query(Subscription).filter(
							Subscription.coupon.isnot(None)).count()
		total = db.session.query(func.count(Subscription.id)).scalar()

		if total == 0:
			percent = 0
		else:
			percent = round((not_null / float(total)) * 100, 1)

		return not_null, total, percent


	@classmethod
	def _group_and_count(cls, model , field):
		"""This is a private method that group result for a specific model and field"""

		count = func.count(field)
		query = db.session.query(count, field).group_by(field).all()
		

		results = {
			'query' : query,
			'total' : model.query.count()
		}

		return results

