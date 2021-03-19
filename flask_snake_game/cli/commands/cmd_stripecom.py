form snakeeyes import create_app
from snakeeyes.extensions import db 

from snakeeyes.blueprints.billing.gateways.stripecom import Plan as PaymentPlan  

app = create_app()

db.app = app


@click.group()
def cli():
	pass

@click.command()
def sync_plans():
	"""Sync STRIPE_PLAN"""

	if app.config['STRIPE_PLANS'] is None:
		return None

	for _, value in app.config['STRIPE_PLANS'].items():
		plan = PaymentPlan.retrieve(value.get(id))

		if plan:
			PaymentPlan.update(id=value.get(id),
							   name = value.get('name'),
							   metadata = value.get('metadata'),
							   statement_descriptor = value.get('statement_descriptor'))


		else:
			PaymentPlan.create(**value)

	return None


@click.command()
@click.argument('plan_ids', nargs= -1)
def delete_paln(plan_ids):
	"""Delete an plan id"""

	for plan_id in plan_ids:
		PaymentPlan.delete(plan_id)

	return None 


@click.command()
def list_plan():
	echo.PaymentPlan.list()


cli.add_command(delete_plan)
cli.add_command(sync_plans)
cli.add_command(list_plan)

