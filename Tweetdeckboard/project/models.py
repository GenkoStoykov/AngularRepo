# project/models.py


import datetime
import json

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from project import db, bcrypt


class Base(db.Model):
    __abstract__ = True

    def to_dict(self, show=None, hide=None, path=None, show_all=None):
        """ Return a dictionary representation of this model.
        """

        if not show:
            show = []
        if not hide:
            hide = []
        hidden = []
        if hasattr(self, 'hidden_fields'):
            hidden = self.hidden_fields
        default = []
        if hasattr(self, 'default_fields'):
            default = self.default_fields

        ret_data = {}

        if not path:
            path = self.__tablename__.lower()

            def prepend_path(item):
                item = item.lower()
                if item.split('.', 1)[0] == path:
                    return item
                if len(item) == 0:
                    return item
                if item[0] != '.':
                    item = '.%s' % item
                item = '%s%s' % (path, item)
                return item

            show[:] = [prepend_path(x) for x in show]
            hide[:] = [prepend_path(x) for x in hide]

        columns = self.__table__.columns.keys()
        relationships = self.__mapper__.relationships.keys()
        properties = dir(self)

        for key in columns:
            check = '%s.%s' % (path, key)
            if check in hide or key in hidden:
                continue
            if show_all or key is 'id' or check in show or key in default:
                ret_data[key] = getattr(self, key)

        for key in relationships:
            check = '%s.%s' % (path, key)
            if check in hide or key in hidden:
                continue
            if show_all or check in show or key in default:
                hide.append(check)
                is_list = self.__mapper__.relationships[key].uselist
                if is_list:
                    ret_data[key] = []
                    for item in getattr(self, key):
                        ret_data[key].append(item.to_dict(
                            show=show,
                            hide=hide,
                            path=('%s.%s' % (path, key.lower())),
                            show_all=show_all,
                        ))
                else:
                    if self.__mapper__.relationships[key].query_class is not None:
                        ret_data[key] = getattr(self, key).to_dict(
                            show=show,
                            hide=hide,
                            path=('%s.%s' % (path, key.lower())),
                            show_all=show_all,
                        )
                    else:
                        ret_data[key] = getattr(self, key)

        for key in list(set(properties) - set(columns) - set(relationships)):
            if key.startswith('_'):
                continue
            check = '%s.%s' % (path, key)
            if check in hide or key in hidden:
                continue
            if show_all or check in show or key in default:
                val = getattr(self, key)
                try:
                    ret_data[key] = json.loads(json.dumps(val))
                except:
                    pass

        return ret_data


class User(Base):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    deck = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, username, password, admin=False, deck=False):
        self.username = username
        self.password = bcrypt.generate_password_hash(password)
        self.registered_on = datetime.datetime.utcnow()
        self.admin = admin
        self.deck = deck

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {0}>'.format(self.username)


class Deck(Base):
    __tablename__ = "decks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    login_code = db.Column(db.Integer, nullable=False)
    email_address = db.Column(db.String(255), nullable=False)
    user_password = db.Column(db.String(255), nullable=False)

    def __init__(self, name, password, user_password, login_code, email_address):
        self.name = name
        self.password = password
        self.user_password = user_password
        self.login_code = login_code
        self.email_address = email_address

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<Deck {0}>'.format(self.name)


class Link(Base):
    __tablename__ = "links"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, ForeignKey(User.id), nullable=False)
    deckid = db.Column(db.Integer, ForeignKey(Deck.id), nullable=False)
    deck = relationship("Deck")
    user = relationship("User")

    def __init__(self, userid, deckid):
        self.userid = userid
        self.deckid = deckid

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<Link {0}>'.format(self.id)


class Profile(Base):
    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    linkid = db.Column(db.Integer, ForeignKey(Link.id), nullable=False)
    keyword = db.Column(db.String(255), nullable=False)
    minutes = db.Column(db.Integer, nullable=False)
    run_status = db.Column(db.Integer, nullable=False)
    last_retweeted = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime)
    tweetid_list = db.Column(db.String(1024))
    last_tweetid = db.Column(db.String(255))
    failed_tweetid_list = db.Column(db.String(1024))
    tweettext_list = db.Column(db.String(8192))
    link = relationship("Link")

    def __init__(self, linkid, keyword, minutes, run_status):
        self.linkid = linkid
        self.keyword = keyword
        self.minutes = minutes
        self.run_status = run_status
        self.created_at = datetime.datetime.utcnow()
        self.tweetid_list = ''
        self.last_tweetid = ''
        self.failed_tweetid_list = ''
        self.tweettext_list = ''

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<Profile {0}>'.format(self.id)


class Approve(Base):
    __tablename__ = "approves"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    linkid = db.Column(db.Integer, ForeignKey(Link.id), nullable=False)
    keyword = db.Column(db.String(255), nullable=False)
    minutes = db.Column(db.Integer, nullable=False)
    approve_status = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime)
    link = relationship("Link")

    def __init__(self, linkid, keyword, minutes, approve_status):
        self.linkid = linkid
        self.keyword = keyword
        self.minutes = minutes
        self.approve_status = approve_status
        self.created_at = datetime.datetime.utcnow()

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<Approve {0}>'.format(self.id)


class Log(Base):
    __tablename__ = "logs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    deckname = db.Column(db.String(255), nullable=False)
    keyword = db.Column(db.String(255), nullable=False)
    retweetid = db.Column(db.String(255), nullable=False)
    last_retweeted = db.Column(db.DateTime)

    def __init__(self, username, deckname, keyword, retweetid):
        self.username = username
        self.deckname = deckname
        self.keyword = keyword
        self.retweetid = retweetid
        self.last_retweeted = datetime.datetime.utcnow()

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<Log {0}>'.format(self.id)


class Adminmail(Base):
    __tablename__ = "adminmail"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email_address = db.Column(db.String(255),unique=True, nullable=False)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    smtpserver = db.Column(db.String(255), nullable=False)

    def __init__(self, email_address,username,password,smtpserver):
        self.email_address = email_address
        self.username = username
        self.password = password
        self.smtpserver = smtpserver

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<Adminmail {0}>'.format(self.name)
