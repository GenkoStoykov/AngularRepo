# project/config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    SECRET_KEY = 'my_precious'
    BCRYPT_LOG_ROUNDS = 13
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db/'
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgresql@localhost:5432/'
    # CHROME_BIN_PATH = os.environ['CHROME_PATH']
    CHROME_BIN_PATH = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    OAUTH_TOKEN = '316545541-AhhNv59dXC6zPziZuSeGALEKcbrRMteqzaRZpenP'
    OAUTH_SECRET = '0idEp1dAGwwmqJ0f9DZT2w19Ty0wulKydD0Gk1ZygEblm'
    CONSUMER_KEY = 'nO67Aw4xv5d42afbVfPVPeOO9'
    CONSUMER_SECRET = 'pdkcLzPAkE2K3mqXgqtsJy8ET7JW9hVq3IN9mGxIX4hNxyPGfD'

    MISFIRE_GRACE_TIME = 30 #seconds

    TEMPLATES_AUTO_RELOAD = True
    PAGE_LOAD_MAXIMUM_TIMEOUT = 20 #seconds
    MINIMUM_INTERVAL_TIME = 10 #seconds