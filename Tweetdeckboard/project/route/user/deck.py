from flask import request, jsonify
from project import db, scheduler
from project.models import Deck, Profile, Link

from . import user_routes


@user_routes.route('/getLinksByUserId', methods=['POST'])  # param : userid
def getLinksByUserId():
    json_data = request.json
    links = (
    db.session.query(Link.id, Link.userid, Link.deckid, Deck.name, Deck.login_code).filter_by(userid=json_data['userid'])
    .join(Deck)).all()
    ret_data = []
    for link in links:
        link_data = {}
        for key in link._fields:
            link_data[key] = getattr(link, key)
        ret_data.append(link_data)
    return jsonify({'result': ret_data})


@user_routes.route('/getDeckById', methods=['POST'])
def getDeckById():
    json_data = request.json
    deck = Deck.query.filter_by(id=json_data['id']).first()
    return jsonify({'result': deck.to_dict(show_all=True)})
