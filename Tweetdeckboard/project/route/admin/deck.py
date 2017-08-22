from apscheduler.triggers.interval import IntervalTrigger
from flask import jsonify, request
from project import app, db, scheduler
from project.models import Deck, Profile, Link, User, Approve
from project.others import is_admin, removedriver, is_running, getdriver, \
    auto_rt, create_driver, login_tweetdeck, adddriver, verify_tweetdeck

from . import admin_routes


@admin_routes.route('/adddeck', methods=['POST'])
def adddeck():
    result = {}
    json_data = request.json
    deck = Deck.query.filter_by(name=json_data['name']).first()
    user = User.query.filter_by(username=json_data['name'], deck=True).first()
    if (deck != None or user != None):
        result['status'] = -1
        result['msg'] = 'Deck is exist already.'
    else:
        try:
            #add deck
            deck = Deck(
                name=json_data['name'],
                password=json_data['password'],
                user_password=json_data['user_password'],
                email_address=json_data['email'],
                login_code=-1
            )
            #add user
            user=User(
                username=json_data['name'],
                password=json_data['user_password'],
                admin=False,
                deck=True
            )
            db.session.add(deck)
            db.session.add(user)
            db.session.commit()
            result['msg'] = 'Succefully Deck added .'
            result['status'] = 1
        except:
            result['msg'] = 'Occured error in db session.'
            result['status'] = -1
        db.session.close()
    return jsonify({'result': result})


@admin_routes.route('/linkdeck', methods=['POST'])
def linkdeck():
    result = {}
    json_data = request.json
    if (is_admin()):
        link = Link(
            userid=json_data['userid'],
            deckid=json_data['deckid']
        )
        try:
            db.session.add(link)
            db.session.commit()
            result['status'] = 1
            result['msg'] = 'Sucessfully linked.'
        except:
            result['msg'] = 'This user is already linked with this deck.'
            result['status'] = 0
    else:
        result['status'] = -1
        result['msg'] = 'Please login now.'
    return jsonify({'result': result})


@admin_routes.route('/unlinkdeck', methods=['POST'])
def unlinkdeck():
    result = {}
    json_data = request.json
    if (is_admin()):
        link = Link.query.filter_by(userid=json_data['userid'], deckid=json_data['deckid']).first()
        if (link == None):
            result['msg'] = 'This user is not linked with this deck.'
            result['status'] = 0
        else:
            try:
                profiles = Profile.query.filter_by(linkid=link.id).all()
                for profile in profiles:
                    if (profile.run_status == 1):
                        jobid = 'retweet_%s' % (profile.id)
                        if (is_running(jobid)):
                            scheduler.remove_job(jobid)
                    db.session.delete(profile)
                approves = Approve.query.filter_by(linkid=link.id).all()
                for approve in approves:
                    db.session.delete(approve)
                db.session.delete(link)
                db.session.commit()
                result['status'] = 1
                result['msg'] = 'Sucessfully unlinked.'
            except:
                result['msg'] = 'Occured error in db session.'
                result['status'] = 0
    else:
        result['status'] = -1
        result['msg'] = 'Please login now.'
    return jsonify({'result': result})


@admin_routes.route('/listDecks', methods=['POST'])
def listDecks():
    result = {}
    if (is_admin()):
        decks = Deck.query.all()
        result['decks'] = [deck.to_dict(show_all=True) for deck in decks]
        result['status'] = 1
    else:
        result['status'] = -1
        result['msg'] = 'Please login now.'
    return jsonify({'result': result})


@admin_routes.route('/delDeck', methods=['POST'])
def delDeck():
    result = {}
    json_data = request.json
    try:
        deck = Deck.query.filter_by(id=json_data['id']).first()
        links = Link.query.filter_by(deckid=deck.id).all()
        user=User.query.filter_by(username=deck.name).first()
        for link in links:
            profiles = Profile.query.filter_by(linkid=link.id).all()
            for profile in profiles:
                if (profile.run_status == 1):
                    jobid = 'retweet_%s' % (profile.id)
                    if (is_running(jobid)):
                        scheduler.remove_job(jobid)
                db.session.delete(profile)
            approves = Approve.query.filter_by(linkid=link.id).all()
            for approve in approves:
                db.session.delete(approve)
            db.session.delete(link)
        removedriver(deck.name)
        db.session.delete(deck)
        db.session.delete(user)
        db.session.commit()
        result['status'] = 1
        result['msg'] = 'Succefully deleted Deck.'
    except:
        result['status'] = -1
        result['msg'] = 'Occured error in delete Deck.'
    db.session.close()
    return jsonify({'result': result})


@admin_routes.route('/logindeck', methods=['POST'])
def logindeck():
    result = {}
    json_data = request.json
    # if (is_admin()):
    deck = Deck.query.filter_by(id=json_data['deckid']).first()
    if (deck == None):
        result['status'] = -1
        result['msg'] = 'Deck is not exist.'
    else:
        driver = create_driver()
        login_code = login_tweetdeck(driver, deck.name, deck.password)['code']
        Deck.query.filter_by(id=json_data['deckid']).update({"login_code": login_code})
        db.session.commit()
        if (login_code < 0):
            driver.quit()
            result['msg'] = 'Unable to login to twitter.'
            result['status'] = -2
        else:
            if (login_code == 0):
                result['status'] = 0
                result['msg'] = 'Please input verification code.'
            else:
                profiles = (
                    db.session.query(Profile.id, Profile.minutes, Link.deckid)
                        .join(Link)).filter_by(deckid=deck.id).all()
                for profile in profiles:
                    scheduler.add_job(
                        func=auto_rt,
                        kwargs={'profile_id': profile.id, 'driver': driver},
                        trigger=IntervalTrigger(minutes=profile.minutes),
                        # trigger=IntervalTrigger(minutes=1)
                        id='retweet_%s' % (profile.id),
                        replace_existing=False,
                        misfire_grace_time=app.config['MISFIRE_GRACE_TIME'])
                    Profile.query.filter_by(id=profile.id).update({"run_status": 1})
                db.session.commit()
                result['msg'] = "Succefully Logged Deck."
                result['status'] = 1
            adddriver(deck.name, driver)
    # else:
    #     result['status'] = -1
    #     result['msg'] = 'Please login now.'
    return jsonify({'result': result})


@admin_routes.route('/verifydeck', methods=['POST'])
def verifydeck():
    result = {}
    json_data = request.json
    deck = Deck.query.filter_by(id=json_data['deckid']).first()
    if (deck == None):
        result['status'] = -1
        result['msg'] = 'Deck does not existed.'
    else:
        driver = getdriver(deck.name)
        if (driver != None):
            login_code = verify_tweetdeck(deck.id, driver, json_data['code'])['code']
            if (login_code == 1):
                Deck.query.filter_by(id=json_data['deckid']).update(
                    {"login_code": login_code})
                profiles = (
                    db.session.query(Profile.id, Profile.minutes, Link.deckid)
                        .join(Link)).filter_by(deckid=deck.id).all()
                for profile in profiles:
                    scheduler.add_job(
                        func=auto_rt,
                        kwargs={'profile_id': profile.id, 'driver': driver},
                        trigger=IntervalTrigger(minutes=profile.minutes),
                        # trigger=IntervalTrigger(minutes=1),
                        id='retweet_%s' % (profile.id),
                        replace_existing=False,
                        misfire_grace_time=app.config['MISFIRE_GRACE_TIME'])
                    Profile.query.filter_by(id=profile.id).update({"run_status": 1})
                db.session.commit()
                result['status'] = 1
                result['msg'] = 'Success Verify Deck Account'
            elif(login_code == 0):
                result['status'] = 0
                result['msg'] = 'Cannot login to tweetdeck. Please check your password.'
            else:
                result['status'] = 0
                result['msg'] = 'Failed verification.'
        else:
            result['status'] = -1
            result['msg'] = 'Driver is not available.'
    return jsonify({'result': result})


@admin_routes.route('/updateDeck', methods=['POST'])
def updateDeck():
    result = {}
    json_data = request.json
    deck = Deck.query.filter_by(id=json_data['id']).first()
    if (deck == None):
        result['status'] = -1
        result['msg'] = 'Deck is not existed.'
    else:
        Deck.query.filter_by(id=json_data['id']).update({
            "email_address": json_data['email_address'],
            "password": json_data['password']
        })
        result['status'] = 1
        result['msg'] = 'Succefully Updated Deck.'
        db.session.commit()
    db.session.close()
    return jsonify({'result': result})