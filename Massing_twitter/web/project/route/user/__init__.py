from flask import Blueprint
user_routes = Blueprint('user_routes', __name__, url_prefix='/user')

from .account import *
from .profile import *
from project import twitter_connection


@user_routes.route('/findUsers', methods=['POST'])
def findUsers():
    result = {}
    json_data = request.json
    results = twitter_connection.users.search(q='%s' % json_data["screen_name"],count=json_data["viewCount"])
    users = []
    for user in results:
        tmpuser = {}
        tmpuser['id'] = user['id'];
        tmpuser['name'] = user['name'];
        tmpuser['screen_name'] = user['screen_name'];
        tmpuser['location'] = user['location'];
        users.append(tmpuser);
    result['users'] = users
    return jsonify({'result': result})