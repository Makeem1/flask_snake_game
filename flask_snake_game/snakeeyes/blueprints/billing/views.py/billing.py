from flask import Blueprint, redirect, url_for, render_template
from config import settings 

billing = Blueprint('billing', __name__, template_folder = '../templates', url_prix = '/subscription')


@billing.route('/pricing')
def pricing():
	if current_user.is_authenticated and current_user.subscription:
		return redirect(url_for('billing.update'))

	form = SubscriptionForm()

	return render_template('billing/pricing.html', form=form, plans=settings.STRIPE_PLANS)