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
    """Function checking for user role"""

    def decorators(f):
        @wraps(f)
        def decorated_fucntions(*args, **kwargs):
            if current_user.role not in roles:
                flash("You do not have permission to visit this page.", 'warning')
                return redirect('/')
            return f(*args, **kwargs)
        return decorated_fucntions
    return decorators
