from flask import Blueprint

billing = Blueprint('billing', __name__, template_folder = '../templates', url_prix = '/subscription')



