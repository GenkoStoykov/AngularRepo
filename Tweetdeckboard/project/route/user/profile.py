from apscheduler.triggers.interval import IntervalTrigger
from flask import jsonify, request
from project import db, scheduler, app
from project.models import Profile, Deck, Link, User, Approve
from project.others import getdriver, auto_rt, is_running, send_email

from . import user_routes


@user_routes.route('/getProfilesByUserId', methods=['POST'])
def getProfilesByUserId():
    json_data = request.json
    profiles = (
        db.session.query(Profile.id, Profile.keyword, Profile.run_status,
                         Profile.minutes, Profile.created_at,
                         Profile.last_retweeted, Link.deckid,
                         Deck.name, User.username)
            .join(Link).join(Deck).join(User)).filter_by(id=json_data['userid']).all()
    ret_data = []
    for profile in profiles:
        prof_data = {}
        for key in profile._fields:
            prof_data[key] = getattr(profile, key)
        ret_data.append(prof_data)
    return jsonify({'result': ret_data})


@user_routes.route('/getProfileById', methods=['POST'])
def getProfileById():
    json_data = request.json
    profile = (
        db.session.query(Profile.id, Deck.name, Profile.linkid, Profile.keyword, Profile.minutes,
                         User.username).filter_by(id=json_data['id'])
            .join(Link).join(User).join(Deck)).first()
    prof_data = {}
    for key in profile._fields:
        prof_data[key] = getattr(profile, key)
    return jsonify({'result': prof_data})


@user_routes.route('/getApprovesByUserId', methods=['POST'])
def getApprovesByUserId():
    json_data = request.json
    approves = (
        db.session.query(Approve.id, Approve.keyword, Approve.approve_status,
                         Approve.minutes, Approve.created_at, Link.deckid,
                         Deck.name, User.username)
            .join(Link).join(Deck).join(User)).filter_by(id=json_data['userid']).all()
    ret_data = []
    for approve in approves:
        prof_data = {}
        for key in approve._fields:
            prof_data[key] = getattr(approve, key)
        ret_data.append(prof_data)
    return jsonify({'result': ret_data})


@user_routes.route('/addApprove', methods=['POST'])
def addApprove():
    result = {}
    json_data = request.json
    minutes = json_data['minutes']
    approve = Approve.query.filter_by(linkid=json_data['linkid'], keyword=json_data['keyword']).first()
    link = Link.query.filter_by(id=json_data['linkid']).join(Deck).first()
    try:
        minutes = int(minutes)
        if (minutes < app.config['MINIMUM_INTERVAL_TIME']):
            result['status'] = 0
            result['msg'] = 'Interval time must to be more than %s minutes' % app.config['MINIMUM_INTERVAL_TIME']
        elif (approve != None):
            result['status'] = -1
            result['msg'] = 'Approve is already existed.'
        elif (link.deck == None):
            result['status'] = -1
            result['msg'] = 'Deck is not available.'
        else:
            approve = Approve(
                linkid=json_data['linkid'],
                keyword=json_data['keyword'],
                minutes=json_data['minutes'],
                approve_status=0
            )
            db.session.add(approve)
            db.session.commit()
            result['status'] = 1
            result['msg'] = 'Succefully submitted request.'

            username = User.query.filter_by(id=link.userid).first().username
            subject = "Deck row is submitted by %s with %s deck account." % (username, link.deck.name)
            msg = "Deck row is submitted by %s with %s , %s minutes" % (
                username, json_data['keyword'], json_data['minutes'])
            send_email(link.deck.email_address, msg, subject)
            # if (send_email(link.deck.email_address, msg, subject) != True):
            #     result['status'] = -1
            #     result['msg'] = 'Fail to send mail.'
    except:
        result['status'] = -1
        result['msg'] = 'Occured error in db session.'
    db.session.close()
    return jsonify({'result': result})
