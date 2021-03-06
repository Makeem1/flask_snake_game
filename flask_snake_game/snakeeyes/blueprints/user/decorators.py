from flask import redirect, flash 
from functools import wraps

from flask_login import current_user

def anonymous_required(url='/settings'):
	"""This function help to prevent the user to visit the login page after login"""  

	def decorator(f):
		@wraps(f)
		def decorated_functions(*args, **kwargs):
			if current_user.is_authenticated:
				flash("Operation already performed", 'info')
				return redirect(url)
			return f(*args, **kwargs)
		return decorated_functions
	return decorator


def role_required(*roles):
	"""Function to check for roles"""
	def decorator(f):
		@wraps
		def decorated_functions(*args, **kwargs):
			if current_user.role not in roles:
				flash("Permission denied, you are not allowed to visit this page.", 'danger')
				return redirect('/')
			return f(*args, **kwargs)
		return decorated_functions
	return decorator
