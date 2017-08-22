from apscheduler.triggers.interval import IntervalTrigger
from flask import jsonify, request
from project import db, scheduler, app
from project.models import User, Profile, Deck, Link
from project.others import is_admin, getdriver, \
    is_running, auto_rt

from . import admin_routes


@admin_routes.route('/listProfiles', methods=['POST'])
def listProfiles():
    result = {}
    if (is_admin()):
        profiles = (
            db.session.query(Profile.id, Profile.keyword, Profile.run_status,
                             Profile.minutes, Profile.created_at,
                             Profile.last_retweeted, Link.deckid,
                             Deck.name, User.username)
                .join(Link).join(Deck).join(User)).all()
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


@admin_routes.route('/addProfile', methods=['POST'])
def addprofile():
    result = {}
    json_data = request.json
    minutes = json_data['minutes']
    profile = Profile.query.filter_by(linkid=json_data['linkid'], keyword=json_data['keyword']).first()
    link = Link.query.filter_by(id=json_data['linkid']).join(Deck).first()
    try:
        minutes = int(minutes)
        if (minutes < app.config['MINIMUM_INTERVAL_TIME']):
            result['status'] = 0
            result['msg'] = 'Interval time must to be more than %s minutes' % app.config['MINIMUM_INTERVAL_TIME']
        elif (profile != None):
            result['status'] = -1
            result['msg'] = 'Profile is already existed.'
        elif (link.deck == None):
            result['status'] = -1
            result['msg'] = 'Deck is not available.'
        else:
            profile = Profile(
                linkid=json_data['linkid'],
                keyword=json_data['keyword'],
                minutes=json_data['minutes'],
                run_status=link.deck.login_code
            )
            db.session.add(profile)
            db.session.commit()
            result['status'] = 1
            result['msg'] = 'Succefully Added Profile.'
            driver = getdriver(link.deck.name)
            if (driver != None):
                if (link.deck.login_code > 0):
                    scheduler.add_job(
                        func=auto_rt,
                        kwargs={'profile_id': profile.id, 'driver': driver},
                        trigger=IntervalTrigger(minutes=profile.minutes),
                        # trigger=IntervalTrigger(minutes=1),
                        id='retweet_%s' % (profile.id),
                        replace_existing=False,
                        misfire_grace_time=app.config['MISFIRE_GRACE_TIME'])
                    Profile.query.filter_by(id=profile.id).update({'run_status': 1})
            else:
                Profile.query.filter_by(id=profile.id).update({'run_status': 0})
                db.session.commit()
                result['status'] = -1
                result['msg'] = 'Driver is not available.'
            #send email
            # username = User.query.filter_by(id=link.userid).first().username
            # subject = "Deck row is submitted by %s with %s deck account." % (username, link.deck.name)
            # msg = "Deck row is submitted by %s with %s , %s minutes" % (
            #     username, json_data['keyword'], json_data['minutes'])
            # if (send_email(link.deck.email_address, msg, subject) != True):
            #     result['status'] = -1
            #     result['msg'] = 'Fail to send mail.'
    except:
        result['status'] = -1
        result['msg'] = 'Occured error in db session.'
    db.session.close()
    return jsonify({'result': result})


@admin_routes.route('/updateProfile', methods=['POST'])
def updateProfile():
    result = {}
    json_data = request.json
    minutes = json_data['minutes']
    profile = Profile.query.filter_by(id=json_data['id']).first()
    link = Link.query.filter_by(id=profile.linkid).join(Deck).first()
    minutes = int(minutes)
    if (minutes < 10):
        result['status'] = 0
        result['msg'] = 'Interval time must to be more than %s minutes' % app.config['MINIMUM_INTERVAL_TIME']
    elif (profile == None):
        result['status'] = -1
        result['msg'] = 'Profile is not existed.'
    elif (link.deck == None):
        result['status'] = -1
        result['msg'] = 'Deck is not available.'
    else:
        Profile.query.filter_by(id=json_data['id']).update({"minutes": json_data['minutes']})
        result['status'] = 1
        result['msg'] = 'Succefully Updated Profile.'
        if (profile.run_status == 1):
            driver = getdriver(link.deck.name)
            if (driver != None):
                jobid = 'retweet_%s' % (profile.id)
                if (is_running(jobid)):
                    scheduler.remove_job(jobid)
                params = {'profile_id': profile.id, 'driver': driver}
                scheduler.add_job(
                    func=auto_rt,
                    kwargs=params,
                    trigger=IntervalTrigger(minutes=minutes),
                    # trigger=IntervalTrigger(minutes=1),
                    id='retweet_%s' % (json_data['id']),
                    replace_existing=False,
                    misfire_grace_time=app.config['MISFIRE_GRACE_TIME'])
                Profile.query.filter_by(id=profile.id).update({'run_status': 1})
            else:
                Profile.query.filter_by(id=profile.id).update({'run_status': 0})
                result['status'] = -1
                result['msg'] = 'Driver is not available.'
        db.session.commit()
    db.session.close()
    return jsonify({'result': result})


@admin_routes.route('/delProfile', methods=['POST'])
def delProfile():
    result = {}
    json_data = request.json
    try:
        profile = Profile.query.filter_by(id=json_data['id']).first()
        if (profile.run_status == 1):
            jobid = 'retweet_%s' % (profile.id)
            if (is_running(jobid)):
                scheduler.remove_job(jobid)
        db.session.delete(profile)
        db.session.commit()
        result['status'] = 1
        result['msg'] = 'Succefully deleted Profile.'
    except:
        result['status'] = -1
        result['msg'] = 'Occured error in delete profile.'
    db.session.close()
    return jsonify({'result': result})


@admin_routes.route('/runProfile', methods=['POST'])
def runProfile():
    result = {}
    json_data = request.json
    profile = Profile.query.filter_by(id=json_data['id']).first()
    link = Link.query.filter_by(id=profile.linkid).join(Deck).first()
    if (profile == None):
        result['status'] = -1
        result['msg'] = 'Profile is not existed.'
    if(link.deck.login_code < 1):
        result['status'] = -1
        result['msg'] = 'Please login or verify deck now.'
    elif (link.deck == None):
        result['status'] = -1
        result['msg'] = 'Deck is not available.'
    else:
        result['status'] = 1
        result['msg'] = 'Succefully run Profile.'
        if (profile.run_status < 1):
            driver = getdriver(link.deck.name)
            if (driver != None):
                jobid = 'retweet_%s' % (profile.id)
                if (is_running(jobid)):
                    scheduler.remove_job(jobid)
                params = {'profile_id': profile.id, 'driver': driver}
                scheduler.add_job(
                    func=auto_rt,
                    kwargs=params,
                    trigger=IntervalTrigger(minutes=profile.minutes),
                    # trigger=IntervalTrigger(minutes=1),
                    id='retweet_%s' % (json_data['id']),
                    replace_existing=False,
                    misfire_grace_time=app.config['MISFIRE_GRACE_TIME'])
                Profile.query.filter_by(id=profile.id).update({'run_status': 1})
            else:
                result['status'] = -1
                result['msg'] = 'Driver is not available.'
        db.session.commit()
    db.session.close()
    return jsonify({'result': result})


@admin_routes.route('/pauseProfile', methods=['POST'])
def pauseProfile():
    result = {}
    json_data = request.json
    profile = Profile.query.filter_by(id=json_data['id']).first()
    link = Link.query.filter_by(id=profile.linkid).join(Deck).first()
    if (profile == None):
        result['status'] = -1
        result['msg'] = 'Profile is not existed.'
    elif (link.deck == None):
        result['status'] = -1
        result['msg'] = 'Deck is not available.'
    else:
        result['status'] = 1
        result['msg'] = 'Succefully Updated Profile.'
        if (profile.run_status == 1):
            jobid = 'retweet_%s' % (profile.id)
            if (is_running(jobid)):
                scheduler.remove_job(jobid)
            Profile.query.filter_by(id=profile.id).update({'run_status': 0})
            db.session.commit()
    db.session.close()
    return jsonify({'result': result})