from lib.util_sqlalchemy import ResourceMixin
from lib.util_datetime import tzware_datetime
from snakeeyes.extensions import db

class Bet(db.Model, ResourceMixin):
	__tablename__ = 'bets'

	id = db.Column(db.Integer(), primary_key=True, index=True)

	# Relationship column with user model 
	user_id = db.Column(db.Integer, db.ForeignKey('user.id', 
													onupdate='CASACDE',
													ondelete='CASCADE'), 
						index=True, nullable=False)

	# Bet details
	guess = db.Column(db.Integer())
	die_1 = db.Column(db.Integer())
	die_2 = db.Column(db.Integer())
	roll = db.Column(db.Integer())
	guess = db.Column(db.Integer())
	wagered = db.Column(db.BigInteger())
	net = db.Column(db.BigInteger())
	payout = db.Column(db.Float())

	def __init__(self, **kwargs):
		# Call Flask-SQLAchemy's constructor.
		super(Bet, self).__init__(**kwargs)

	@classmethod 
	def is_winner(cls, guess, roll):
		"""
		Determine if the result is a win or loss 
		:param guess: Dice guess
		:param type: int
		:param roll: Dice roll 
		:param type: int
		:return: bool  
		"""

		if guess == roll:
			return True 

		return False

	@classmethod
	def determine_payout(cls, payout, is_winner):
		"""
		Determine the payout.

		:param payout: Dice guess
		:type param :float
		:param is_winner: was the bet won or lost 
		:type param : bool
		:return: int
		"""

		if is_winner:
			return payout

		return 1.0


	@classmethod
	def calculate(cls, wagered, payout, is_winner):
		"""
		Calculate the net won or lost 
		:param wagered: Dice guess
		:type wagered: int
		:param payout: Dice roll
		:type payout: float
		:param is_winner: was the bet won or lost 
		:type is_winner: bool
		:return: int
		"""

		if is_winner:
			return int(wagered * payout)

		return -wagered


	def save_and_update_user(self, user):
		"""
		Commit the bet and update the user's information 
		:return : SQLAlchemy save result
		"""

		self.save()

		user.coins += self.net
		user.last_bet_on = tzware_datetime()
		return user.save()

	






