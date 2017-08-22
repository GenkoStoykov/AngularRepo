from apscheduler.triggers.interval import IntervalTrigger
from flask import jsonify, request
from project import app, db, scheduler
from project.models import User, Profile, Deck, Link, Approve
from project.others import is_deck, is_running, getdriver, auto_rt

from . import deck_routes


@deck_routes.route('/getProfilesByDeckname', methods=['POST'])
def getProfilesByDeckname():
    json_data = request.json
    result = {}
    if (is_deck()):
        profiles = (
            db.session.query(Profile.id, Profile.keyword, Profile.run_status,
                             Profile.minutes, Profile.created_at,
                             Profile.last_retweeted, Link.deckid,
                             Deck.name, User.username)
                .join(Link).join(Deck).filter_by(name=json_data['name']).join(User)).all()
        ret_data = []
        for profile in profiles:
            profile_data = {}
            for key in profile._fields:
                profile_data[key] = getattr(profile, key)
            ret_data.append(profile_data)
        result['status'] = 1
        result['profiles'] = ret_data
    else:
        result['status'] = -1
        result['msg'] = 'Please login now.'
    return jsonify({'result': result})


@deck_routes.route('/getApproveByDeckname', methods=['POST'])
def getApproveByDeckname():
    json_data = request.json
    result = {}
    if (is_deck()):
        approves = (
            db.session.query(Approve.id, Approve.keyword, Approve.approve_status,
                             Approve.minutes, Approve.created_at,  Link.deckid,
                             Deck.name, User.username)
                .join(Link).join(Deck).filter_by(name=json_data['name']).join(User)).all()
        ret_data = []
        for approve in approves:
            profile_data = {}
            for key in approve._fields:
                profile_data[key] = str(getattr(approve, key))
            ret_data.append(profile_data)
        result['status'] = 1
        result['approves'] = ret_data
    else:
        result['status'] = -1
        result['msg'] = 'Please login now.'
    return jsonify({'result': result})


@deck_routes.route('/declinePendingById', methods=['POST'])
def declinePendingById():
    json_data = request.json
    result = {}
    if (is_deck()):
        try:
            Approve.query.filter_by(id=json_data['id']).update({'approve_status':-1})
            db.session.commit()
            result['status'] = 1
            result['msg'] = 'Succefully declined request.'
        except:
            result['status'] = 0
            result['msg'] = 'Occured error in db session.'
    else:
        result['status'] = -1
        result['msg'] = 'Please login now.'
    return jsonify({'result': result})


@deck_routes.route('/acceptPendingById', methods=['POST'])
def acceptPendingById():
    json_data = request.json
    result = {}
    approve = Approve.query.filter_by(id=json_data['id']).first()
    if(approve == None):
        result['status'] = -1
        result['msg'] = 'Approve is not existed.'
    else:
        if (is_deck()):
            try:
                link = Link.query.filter_by(id=approve.linkid).join(Deck).first()
                profile = Profile.query.filter_by(linkid=link.id, keyword=approve.keyword).first()
                if (link.deck == None):
                    result['status'] = -1
                    result['msg'] = 'Deck is not available.'
                else:
                    if (profile != None):
                        Profile.query.filter_by(id=profile.id).update({"minutes": approve.minutes})
                        result['status'] = 1
                        result['msg'] = 'Succefully added request to profile.'
                        if (profile.run_status == 1):
                            driver = getdriver(link.deck.name)
                            if (driver != None):
                                jobid = 'retweet_%s' % (profile.id)
                                if (is_running(jobid)):
                                    scheduler.remove_job(jobid)
                                params = {'profile_id': profile.id, 'driver': driver}
                                scheduler.add_job(
                                    func=auto_rt,
                                    kwargs={'profile_id': profile.id, 'driver': driver},
                                    trigger=IntervalTrigger(minutes=approve.minutes),
                                    # trigger=IntervalTrigger(minutes=1),
                                    id='retweet_%s' % (profile.id),
                                    replace_existing=False,
                                    misfire_grace_time=app.config['MISFIRE_GRACE_TIME'])
                                Profile.query.filter_by(id=profile.id).update({'run_status': 1})
                            else:
                                Profile.query.filter_by(id=profile.id).update({'run_status': 0})
                                result['status'] = -1
                                result['msg'] = 'Driver is not available.'
                        db.session.delete(approve)
                        db.session.commit()
                    else:
                        newprofile = Profile(
                            linkid=link.id,
                            keyword=approve.keyword,
                            minutes=approve.minutes,
                            run_status=link.deck.login_code
                        )
                        db.session.add(newprofile)
                        db.session.delete(approve)
                        db.session.commit()
                        result['status'] = 1
                        result['msg'] = 'Succefully added request to profile.'
                        driver = getdriver(link.deck.name)
                        if (driver != None):
                            if (link.deck.login_code > 0):
                                scheduler.add_job(
                                    func=auto_rt,
                                    kwargs={'profile_id': newprofile.id, 'driver': driver},
                                    trigger=IntervalTrigger(minutes=approve.minutes),
                                    # trigger=IntervalTrigger(minutes=1),
                                    id='retweet_%s' % (newprofile.id),
                                    replace_existing=False,
                                    misfire_grace_time=app.config['MISFIRE_GRACE_TIME'])
                        else:
                            Profile.query.filter_by(id=newprofile.id).update({'run_status':0})
                            db.session.commit()
                            result['status'] = -1
                            result['msg'] = 'Driver is not available.'
            except:
                result['status'] = 0
                result['msg'] = 'Occured error in db session.'
        else:
            result['status'] = -1
            result['msg'] = 'Please login now.'
    return jsonify({'result': result})

