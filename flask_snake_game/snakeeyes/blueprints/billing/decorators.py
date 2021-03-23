import flask 
from flask import flash, url_for, redirect
from functools import wraps
import stripe



def handle_stripe_exceptions(f):
	"""Function to handle all stripe error inorder to prevent our from 500s error"""

	@wraps(f)
	def decorated_function(*args, **kwargs):
		"""Stripe error"""

		try:
			return f(*args, **kwargs)
		except stripe.error.CardError as e:
			flash('Sorry, your card was declined. Try again perhaps?', 'error')
			return redirect(url_for('user.settings'))
		except stripe.error.InvalidRequestError as e:
			flash(e, 'error')
			return redirect(url_for('user.settings'))
		except stripe.error.AuthenticationError:
			flash('Authentication with our payment gateway failed.', 'error')
			return redirect(url_for('user.settings'))
		except stripe.error.APIConnectionError:
			flash(
                'Our payment gateway is experiencing connectivity issues'
                ', please try again.', 'error')
			return redirect(url_for('user.setting'))
		except stripe.error.StripeError:
			flash(
                'Our payment gateway is having issues, please try again.',
                'error')
			return redirect(url_for('user.settings'))

		return decorated_function