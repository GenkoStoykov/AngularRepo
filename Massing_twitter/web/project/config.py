# project/config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    SECRET_KEY = 'my_precious'
    BCRYPT_LOG_ROUNDS = 13
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db/'
    DEBUG = True

    UPLOAD_FOLDER = 'project/uploads'
    ALLOWED_EXTENSIONS = set(['txt', 'csv'])

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True
    PAGE_LOAD_MAXIMUM_TIMEOUT = 20 #seconds
    MINIMUM_INTERVAL_TIME = 10 #seconds

    # Test

    # SQLAlchemy
    POSTGRES_USER = 'postgres'
    POSTGRES_PASSWORD = 'postgresql'
    POSTGRES_DB = 'massing'
    SQLALCHEMY_DATABASE_URI = 'postgresql://' + POSTGRES_USER + ':' + POSTGRES_PASSWORD + '@localhost:5432/' + POSTGRES_DB

    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_ENABLE_UTC = True
    CELERY_TIMEZONE = 'UTC'

    OAUTH_TOKEN = '316545541-SCeXIu1LrydaHFn11ineJ0Mf50jOgZnzwxx8j3K2'
    OAUTH_SECRET = 'dJzSPmK4gGhvQXGB1xv6yYx7kFLBEb0xizOd7bU4yTIBB'
    CONSUMER_KEY = 'R94B9hVYdTJVg4uqG6TIsVzyf'
    CONSUMER_SECRET = 'zA0dsfdhj9I1cJknczGQRUXj0jwEY5OPR16uY7sCx97tjrsJlu'

    TASK_PERIOD_TIME = 1   #  minutes
    UNFOLLOWING_PERIOD_WEEK = 6 #day of week
    UNFOLLOWING_TASK_HOUR = 9 # UTC hour
    UNFOLLOWING_TASK_MIN = 38  # UTC hour

    # Heroku
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    # CELERY_RESULT_BACKEND = os.environ['REDIS_URL'] + '/0'
    # CELERY_BROKER_URL = os.environ['REDIS_URL'] + '/0'

    # OAUTH_TOKEN = '316545541-2myGCkn6obm26qkg5DAoAPynVoJVBj0FYBvI96Iy'
    # OAUTH_SECRET = 'fvYrL9SLScppu5Q7BKCEE1jHOtVAFDzMSFfL33AdnwwHB'
    # CONSUMER_KEY = '1t4fxXo9PKMgNNzyMCYWloZNa'
    # CONSUMER_SECRET = 'wNJhcYODKGWVxl1pYR4BsnWcSJJlg43zG5utRFodS6Sjqniqss'
