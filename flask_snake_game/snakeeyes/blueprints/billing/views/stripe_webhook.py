from flask import Blueprint

stripe_webhook = Blueprint('stripe_webhook', __name__, url_prefix = '/stripe_webhook')


