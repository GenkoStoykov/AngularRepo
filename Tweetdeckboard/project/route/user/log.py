from flask import jsonify, request
from project.models import Profile, Deck, Link, User,Log
from . import user_routes


@user_routes.route('/getLogs', methods=['POST'])
def getLogs():
    json_data = request.json

    ret_data = []
    if (json_data['logtype'] == 'deck'):
        filter_str = {'deckname': json_data['name']}
    elif (json_data['logtype'] == 'user'):
        filter_str = {'keyword': json_data['name']}
    else:
        pass
    logs = Log.query.filter_by(**filter_str).all()
    return jsonify({'result': [log.to_dict(show_all=True) for log in logs] })