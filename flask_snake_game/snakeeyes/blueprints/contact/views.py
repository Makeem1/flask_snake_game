from flask import (
	Blueprint,
	request,
	url_for, 
	render_template,
	flash, 
	redirect
)
from flask_login import current_user

from snakeeyes.blueprints.contact.forms import ContactForm


contact = Blueprint('contact', __name__, template_folder='templates')


@contact.route('/contact', methods=['GET', 'POST'])
def index():
	"""Prepopulate the form if current user is signed in."""
	form = ContactForm(obj=current_user) 
	if form.validate_on_submit():
		"""Import here to prevent circular import """
		
		from snakeeyes.blueprints.contact.tasks import deliver_contact_email
		email = form.email.data
		message = form.message.data
		data={'email': email, 'message':message}
		deliver_contact_email.delay(email, message)
		flash('Thanks, expect a response soon.', 'success')
		return redirect(url_for('contact.index'))
	return render_template("contact/index.html", form = form)




