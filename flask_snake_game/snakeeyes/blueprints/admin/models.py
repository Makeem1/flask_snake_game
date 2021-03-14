from snakeeyes.blueprints.user.models import User
from snakeeyes.extensions import db
from sqlalchemy import func


class Dashboard(object):
	@classmethod
	def group_and_count_users(cls):
		"""Provide a group and count on all user"""
		return Dashboard._group_and_count_users(User, User.role)


	@classmethod
	def _group_and_count_users(cls, model , field):
		"""This is a private method that group result for a specific model and field"""

		count = func.count(field)
		query = db.session.query(count, field).group_by(field).all()
		

		results = {
			'query' : query,
			'total' : model.query.count()
		}

		return results