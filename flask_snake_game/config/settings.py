from datetime import timedelta

DEBUG = True
LOG_LEVEL = 'DEBUG'

SERVER_NAME = 'localhost:8000'

SECRET_KEY = 'hellowrodjkadyggcwffkuwhneuedxkewhig'

# Email Configuration settings
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = '587'
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'patrickpwilliamson9@gmail.com'  # This email is not correct and will be overwritten by instance file
MAIL_PASSWORD = 'Olayinka1'  # This password is not and will be overwritten by instance settings file
MAIL_DEFAULT_SENDER = 'patrickpwilliamson9@gmail.com'
FLASKY_MAIL_SUBJECT_PREFIX = '[Snakeeyes]'
FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'


# Celery configuration 
CELERY_BROKER_URL = "redis://:olayinka@redis:6379/0"   #broker , password:olayinka and host:redis port:6379 database for redis : 0 
CELERY_RESULT_BACKEND = "redis://:olayinka@redis:6379/0" #backend, password:olayinka and host:redis port:6379 database for redis : 0 
CELERY_ACCEPT_CONTENT = ['json'] # accept only json data
CELERY_TASK_SERIALIZER = 'json' # serialize json data
CELERY_RESULT_SERIALIZER = 'json' # give the result as json data
CELERY_REDIS_MAX_CONNECTIONS = 5  # maximum connection  


# SQLALCHEMY
db_uri = 'postgresql://snakeeyes:devpassword@postgres:5432/snakeeyes'  # first snakeeyes --> user while second snakeeyes --> database name
SQLALCHEMY_DATABASE_URI = db_uri
SQLALCHEMY_TRACK_MODIFICATIONS = False

# User 
SEED_ADMIN_EMAIL = 'dev@local.host'
SEED_ADMIN_PASSWORD = 'devpassword'
REMEMBER_COOKIE_DURATION = timedelta(days=90)


STRIPE_SECRET_KEY = None
STRIPE_PUBLISHABLE_KEY = None
STRIPE_API_VERSION = '2016-03-07'
STRIPE_PLANS = {
    '0': {
        'id': 'bronze',
        'name': 'Bronze',
        'amount': 100,
        'currency': 'usd',
        'interval': 'month',
        'interval_count': 1,
        'trial_period_days': 14,
        'statement_descriptor': 'SNAKEEYES BRONZE',
        'metadata': {}
    },
    '1': {
        'id': 'gold',
        'name': 'Gold',
        'amount': 500,
        'currency': 'usd',
        'interval': 'month',
        'interval_count': 1,
        'trial_period_days': 14,
        'statement_descriptor': 'SNAKEEYES GOLD',
        'metadata': {
            'recommended': True
        }
    },
    '2': {
        'id': 'platinum',
        'name': 'Platinum',
        'amount': 1000,
        'currency': 'usd',
        'interval': 'month',
        'interval_count': 1,
        'trial_period_days': 14,
        'statement_descriptor': 'SNAKEEYES PLATINUM',
        'metadata': {}
    }
}













