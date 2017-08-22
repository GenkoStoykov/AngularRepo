from flask import Blueprint
deck_routes = Blueprint('deck_routes', __name__, url_prefix='/deck')

from .user import *
from .profile import *
