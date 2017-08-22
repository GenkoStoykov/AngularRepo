from flask import request, jsonify
from project import db, scheduler, bcrypt
from project.models import User, Profile, Deck, Log, Link, Adminmail
from project.others import is_deck, removedriver, is_running,getdriver
from project.route.admin.deck import logindeck
from . import deck_routes


@deck_routes.route('/getUsersByDeckname', methods=['POST'])
def getUsersByDeckname():
    json_data = request.json
    result = {}
    if (is_deck()):
        deck = Deck.query.filter_by(name=json_data['name']).first()
        links = Link.query.filter_by(deckid=deck.id).join(User).all()
        ret_data = []
        for link in links:
            user_data = {}
            user_data['id'] = link.user.id
            user_data['username'] = link.user.username
            user_data['registered_on'] = link.user.registered_on
            ret_data.append(user_data)
        result['status'] = 1
        result['users'] = ret_data
    else:
        result['status'] = -1
        result['msg'] = 'Please login now.'
    return jsonify({'result': result})


@deck_routes.route('/getDeckByUsername', methods=['POST'])
def getDeckByUsername():
    json_data = request.json
    result = {}
    if (is_deck()):
        deck = Deck.query.filter_by(name=json_data['name']).first()
        result['status'] = 1
        result['deck'] = deck.to_dict(show_all=True)
    else:
        result['status'] = -1
        result['msg'] = 'Please login now.'
    return jsonify({'result': result})


@deck_routes.route('/changeDeckPass', methods=['POST'])
def changeDeckPass():
    result = {}
    json_data = request.json
    deck = Deck.query.filter_by(id=json_data['deckid']).first()
    if (deck == None):
        result['status'] = -1
        result['msg'] = 'Deck does not existed.'
    else:
        Deck.query.filter_by(id=json_data['deckid']).update({
            "password": json_data['newpass']
        })
        result['status'] = 1
        result['msg'] = 'Succefully Updated Password.'
        db.session.commit()
        if(not getdriver(deck.name)):
            logindeck()
    db.session.close()
    return jsonify({'result': result})