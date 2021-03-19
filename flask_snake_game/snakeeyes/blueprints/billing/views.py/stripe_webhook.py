from flask import Blueprint

stripe_webhook = Blueprint('billing', __name__, url_prix = '/stripe_webhook')


