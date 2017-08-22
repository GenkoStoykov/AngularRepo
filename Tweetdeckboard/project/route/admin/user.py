from flask import request, jsonify
from project import db, scheduler, bcrypt
from project.models import User, Profile, Deck, Log, Link, Adminmail,Approve
from project.others import is_admin, removedriver, is_running

from . import admin_routes


@admin_routes.route('/addUser', methods=['POST'])
def addUser():
    result = {}
    json_data = request.json
    user = User(
        username=json_data['name'],
        password=json_data['password']
    )
    try:
        db.session.add(user)
        db.session.commit()
        result['status'] = 1
        result['msg'] = 'Sucessfully registered.'
    except:
        result['msg'] = 'This user is already registered.'
        result['status'] = 0
    db.session.close()
    return jsonify({'result': result})


@admin_routes.route('/changeAdminPass', methods=['POST'])
def changeAdminPass():
    result = {}
    json_data = request.json
    user = User.query.filter_by(username='admin').first()
    if user and bcrypt.check_password_hash(
            user.password, json_data['oldpass']):
        newpass = bcrypt.generate_password_hash(json_data['newpass'])
        User.query.filter_by(username='admin').update({"password": newpass})
        db.session.commit()
        result['status'] = 1
        result['msg'] = 'Succefully changed password.'
    else:
        result['status'] = -1
        result['msg'] = 'Incorrect password.'
    return jsonify({'result': result})


@admin_routes.route('/setEmail', methods=['POST'])
def setEmail():
    result = {}
    json_data = request.json
    if (is_admin()):
        num_rows_deleted = db.session.query(Adminmail).delete()
        mail = Adminmail(
            email_address=json_data['email'],
            username=json_data['username'],
            password=json_data['password'],
            smtpserver=json_data['smtpserver'],
        )
        db.session.add(mail)
        db.session.commit()
        result['status'] = 1
        result['msg'] = 'Succefully set email address.'
    else:
        result['status'] = -1
        result['msg'] = 'Please login now.'
    return jsonify({'result': result})


@admin_routes.route('/checkEmail')
def checkEmail():
    result = {}
    if (is_admin()):
        mail = Adminmail.query.first()
        if (mail != None):
            result['status'] = 1
            result['msg'] = 'Email Address is setted.'
        else:
            result['status'] = 0
            result['msg'] = 'Email Address is not setted now.'
    else:
        result['status'] = -1
        result['msg'] = 'Please login now.'
    return jsonify({'result': result})


@admin_routes.route('/listUsers', methods=['POST'])
def listUsers():
    result = {}
    if (is_admin()):
        users = User.query.filter_by(admin=False,deck=False).all()
        ret_data = []
        for user in users:
            linked_decks = Link.query.filter_by(userid=user.id).all()
            user_data = {}
            user_data['id'] = user.id
            user_data['username'] = user.username
            user_data['registered_on'] = user.registered_on
            if(len(linked_decks) > 0):
                user_data['linked_decks'] = [link.deckid for link in linked_decks]
            else:
                user_data['linked_decks'] = []
            ret_data.append(user_data)
        result['status'] = 1
        result['users'] = ret_data
    else:
        result['status'] = -1
        result['msg'] = 'Please login now.'
    return jsonify({'result': result})


@admin_routes.route('/delUser', methods=['POST'])  # param: userid
def delUser():
    result = {}
    json_data = request.json
    if (is_admin()):
        try:
            user = User.query.filter_by(id=json_data['userid']).first()
            links = Link.query.filter_by(userid=user.id).all()
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
            db.session.delete(user);
            db.session.commit()
            result['status'] = 1
            result['msg'] = 'Succefully deleted user.'
        except:
            result['status'] = -1
            result['msg'] = 'Occured error in delete user.'
    else:
        result['status'] = -1
        result['msg'] = 'Please login now.'
    db.session.close()
    return jsonify({'result': result})
