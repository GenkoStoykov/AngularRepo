from flask import Blueprint
user_routes = Blueprint('user_routes', __name__, url_prefix='/user')

from .deck import *
from .profile import *
from .log import *