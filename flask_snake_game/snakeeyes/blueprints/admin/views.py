from flask import render_template, Blueprint

from flask_login import login_required
from snakeeyes.blueprints.user.decorators import role_required
from snakeeyes.blueprints.admin.models import Dashboard


admin = Blueprint('admin', __name__,
                  template_folder='templates', url_prefix='/admin')


@admin.before_request
@login_required
@role_required('admin')
def before_request():
	"""
	activity :: This function must run before any other function below is run and all condition must be met.
	protect all admin pages
	"""
	pass


@admin.route('')
def dashboard():
	group_and_count_users = Dashboard.group_and_count_users()
	return render_template('admin/page/dashboard.html', group_and_count_users=group_and_count_users)


