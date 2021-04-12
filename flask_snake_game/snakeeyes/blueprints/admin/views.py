from flask import render_template, Blueprint, request, flash, redirect, url_for


from flask_login import login_required
from snakeeyes.blueprints.user.decorators import role_required
from snakeeyes.blueprints.admin.models import Dashboard
from snakeeyes.blueprints.admin.form import SearchForm , BulkDeleteForm, UserForm, UserCancelSubscriptionForm, CouponForm
from snakeeyes.blueprints.user.models import User
from sqlalchemy import text
from flask_login import current_user
from snakeeyes.blueprints.billing.models.subscription import Subscription
from snakeeyes.blueprints.billing.models.coupon import Coupon
from snakeeyes.extensions import db 
from snakeeyes.blueprints.billing.decorators import handle_stripe_exceptions


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
  group_and_count_plans = Dashboard.group_and_count_plans()
  group_and_count_coupons = Dashboard.group_and_count_coupons()
  return  render_template('admin/page/dashboard.html', 
      group_and_count_users = group_and_count_users,
      group_and_count_coupons = group_and_count_coupons,
      group_and_count_plans = group_and_count_plans)


@admin.route('/users', defaults={'page': 1})
@admin.route('/users/page/<int:page>')
def users(page):
    search_form = SearchForm()
    bulk_form = BulkDeleteForm()

    sort_by = User.sort_by(request.args.get('sort', 'created_on'),
                           request.args.get('direction', 'desc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    paginated_users = User.query \
        .filter(User.search(request.args.get('q', ''))) \
        .order_by(User.role.asc(), text(order_values)) \
        .paginate(page, 50, True)

    return render_template('admin/user/index.html',
                           form=search_form, bulk_form=bulk_form,
                           users=paginated_users)



@admin.route('/users/edit/<int:id>', methods=['GET', 'POST'])
def users_edit(id):
    user = User.query.get(id)
    form = UserForm(obj=user)

    if form.validate_on_submit():
        if User.is_last_admin(user,
                              request.form.get('role'),
                              request.form.get('active')):
            flash('You are the last admin, you cannot do that.', 'error')
            return redirect(url_for('admin.users'))

        form.populate_obj(user)

        if not user.username:
            user.username = None

        user.save()

        flash('User has been saved successfully.', 'success')
        return redirect(url_for('admin.users'))

    return render_template('admin/user/edit.html', form=form, user=user)


@admin.route('/users/bulk_delete', methods=['POST'])
def users_bulk_delete():
    form = BulkDeleteForm()

    if form.validate_on_submit():
        ids = User.get_bulk_action_ids(request.form.get('scope'),
                                       request.form.getlist('bulk_ids'),
                                       omit_ids=[current_user.id],
                                       query=request.args.get('q', ''))


        # Import delete_users here prevent circular import 
        from snakeeyes.blueprints.billing.tasks import delete_users

        delete_count = User.bulk_delete(ids)

        flash('{0} user(s) were scheduled to be deleted.'.format(delete_count),
              'success')
    else:
        flash('No users were deleted, something went wrong.', 'error')

    return redirect(url_for('admin.users'))


@admin.route('/users/cancel_subscription', methods=['POST'])
def users_cancel_subscription():
    form = UserCancelSubscriptionForm()

    if form.validate_on_submit():
        user = db.session.query(User).get(request.form.get('id'))

        if user:
            subscription = Subscription()
            if subscription.cancel(user):
                flash('Subscription has been cancelled for {0}'.format(user.name), 'success' )
            else:
              flash('No subscription was cancelled', 'error')

    return redirect(url_for('admin.users'))


# Coupons -----------------------------------------------------------------------------------------------------

@admin.route('/coupons', defaults={'page':1})
@admin.route('/coupons/page/<int:page>')
def coupon(page):
    search = SearchForm()
    bulk_form = BulkDeleteForm()

    sort_by = Coupon.sort_by(request.args.get('sort', 'created_on'),
                              request.args.get('direction', 'ASC'))

    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    paginated_coupons = Coupon.query.filter(Coupon.search(request.args.get('id', ''))).order_by(text(order_values)).paginate(page, 50, True)

    return render_template('admin/coupon/index.html',
                           form=search, bulk_form=bulk_form,
                           coupons=paginated_coupons)


@admin.route('/coupons/new', methods=['GET', 'POST'])
@handle_stripe_exceptions
def coupons_new():
    coupon = Coupon()
    form = CouponForm(obj=coupon)

    if form.validate_on_submit():
        form.populate_obj(coupon)

        params = {
            'code': coupon.code,
            'duration': coupon.duration,
            'percent_off': coupon.percent_off,
            'amount_off': coupon.amount_off,
            'currency': coupon.currency,
            'redeem_by': coupon.redeem_by,
            'max_redemptions': coupon.max_redemptions,
            'duration_in_months': coupon.duration_in_months,
        }

        if Coupon.create(params):
            flash('Coupon has been created successfully.', 'success')
            return redirect(url_for('admin.coupon'))

    return render_template('admin/coupon/new.html', form=form, coupon=coupon)


@admin.route('/coupons/bulk_delete', methods=['POST'])
def coupon_bulk_delete():
    form = BulkDeleteForm()

    if form.validate_on_submit():
        ids = Coupon.get_bulk_action_ids(request.form.get('scope'),
                                        request.form.getlist('bulk_id'),
                                        query=request.args.get('q', ''))

        from snakeeyes.blueprints.billing.tasks import delete_coupons

        delete_coupons.dalay(ids)

        flash("{0} coupons(s) were scheduled to be deleted.", 'success')

    else:
        flash('No coupons were deleted, something went wrong', 'error')

    return redirect(url_for('admin.coupons'))


