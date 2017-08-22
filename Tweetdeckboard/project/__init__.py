# project/__init__.py

from __future__ import print_function

import atexit
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy
from apscheduler.executors.pool import ProcessPoolExecutor
from config import BaseConfig

# config
drivermap = {}

app = Flask(__name__)
app.config.from_object(BaseConfig)
scheduler = BackgroundScheduler()
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
logging.basicConfig()

from others import *
from route import *
from route.admin import *
from route.deck import *
from route.user import *


def configure_blueprints(blueprints):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def init_app():
    """Create a Flask app."""

    blueprints = [
        routes,
        admin_routes,
        deck_routes,
        user_routes
    ]
    configure_blueprints(blueprints)

    executors = {
        'default': {'type': 'threadpool', 'max_workers': 1},
        'processpool': ProcessPoolExecutor(max_workers=1)
    }

    scheduler.configure(executors=executors)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    atexit.register(close_opened_browser)
    return app

init_app()


@app.before_first_request
def initialize():
    setup_scheduler()


if __name__ == "__main__":
    app.run()