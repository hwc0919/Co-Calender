import datetime
import math
import random
import traceback

from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .mvm import Friendship, UserSchlist, FriendReq

__all__ = ['User', 'Role', 'Schedule', 'Schlist',
           'Friendship', 'UserSchlist', 'FriendReq', '_tables']


class DataUtils(object):
    @staticmethod
    def gen_id(dbname, col_name):
        """Generate a at-least-5-digit unique number"""
        def wrapper():
            model = _tables[dbname]
            n_entries = model.query.count()
            k = max(int(math.log10(n_entries * 2 + 1)), 5)
            while True:
                L = [random.choice(range(1, 10))] + random.choices(range(10), k=k - 1)
                random_id = int(''.join(map(str, L)))
                if not model.query.filter_by(**{col_name: random_id}).first():
                    return random_id
        return wrapper


class SchPrivacy(object):
    SELF = 0
    FRIEND = 1
    GROUP = 2
    CHOOSE = 3
    ALL = 10


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'UTF8MB4'}

    _id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, unique=True, nullable=False, index=True,
                    default=DataUtils.gen_id('users', 'uid'))
    username = db.Column(db.String(32), unique=True, nullable=False, index=True)
    nickname = db.Column(db.String(32), unique=True, default=username, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles._id'))
    password_hash = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(16), unique=True, index=True)
    email = db.Column(db.String(32), unique=True, index=True)
    gender = db.Column(db.Enum('M', 'F', ''), default='')
    age = db.Column(db.SmallInteger)
    register_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    frigroups = db.Column(db.PickleType, nullable=False, default=['默认分组'])

    # OvM
    schedules = db.relationship('Schedule', backref='owner', lazy='dynamic')
    own_lists = db.relationship('Schlist', backref='owner', lazy='dynamic')

    # MvM
    attends = db.relationship('UserSchlist',
                              foreign_keys=[UserSchlist.uid],
                              backref=db.backref('member', lazy='joined'),
                              lazy='dynamic',
                              cascade='all, delete-orphan')

    friends = db.relationship('Friendship',
                              foreign_keys=[Friendship.from_uid],
                              backref=db.backref('from_user', lazy='joined'),
                              lazy='dynamic',
                              cascade='all, delete-orphan')

    as_friends = db.relationship('Friendship',
                                 foreign_keys=[Friendship.to_uid],
                                 backref=db.backref('to_user', lazy='joined'),
                                 lazy='dynamic',
                                 cascade='all, delete-orphan')

    sent_frireqs = db.relationship('FriendReq',
                                   foreign_keys=[FriendReq.from_uid],
                                   backref=db.backref('from_user', lazy='joined'),
                                   lazy='dynamic',
                                   cascade='all, delete-orphan')
    recv_frireqs = db.relationship('FriendReq',
                                   foreign_keys=[FriendReq.to_uid],
                                   backref=db.backref('to_user', lazy='joined'),
                                   lazy='dynamic',
                                   cascade='all, delete-orphan')

    # sent_schreqs
    # recv_schreqs

    def __init__(self, role='user', **kwargs):
        super(User, self).__init__(**kwargs)
        if isinstance(role, str):
            role = Role.query.filter_by(name=role).first()
        self.role = role

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def add_user(user):
        try:
            db.session.add(user)
            db.session.commit()
            return True
        except Exception as ex:
            traceback.print_exc()
            db.session.rollback()
            return False

    def has_friend(self, user):
        uid = user if isinstance(user, int) else user.uid
        return self.friends.filter_by(to_uid=uid).first() is not None

    def add_friend(self, user):
        """Add bi-directional relations in `Friendship`"""
        to_uid = user if isinstance(user, int) else user.uid
        from_uid = self.uid
        try:
            f1 = Friendship(from_uid=from_uid, to_uid=to_uid)
            f2 = Friendship(from_uid=to_uid, to_uid=from_uid)
            db.session.add_all([f1, f2])
            db.session.commit()
            return True
        except Exception as ex:
            db.session.rollback()
            traceback.print_exc()
            return False

    def drop_friend(self, user):
        """Drop bi-directional relations in `Friendship`"""
        to_uid = user if isinstance(user, int) else user.uid
        try:
            self.friends.filter_by(to_uid=to_uid).delete(synchronize_session=False)
            self.as_friends.filter_by(from_uid=to_uid).delete(synchronize_session=False)
            db.session.commit()
            return True
        except Exception as ex:
            db.session.rollback()
            traceback.print_exc()
            return False

    def add_schedule(self, schedule):
        schedule.owner = self
        try:
            db.session.commit()
            return True
        except Exception as ex:
            db.session.rollback()
            traceback.print_exc()
            return False

    def send_frireq(self, user):
        to_uid = user if isinstance(user, int) else user.uid
        req = self.sent_frireqs.filter_by(to_uid=to_uid).first()
        if req is None:
            req = FriendReq(from_uid=self.uid, to_uid=to_uid)
        else:
            req.create_dt = datetime.datetime.utcnow()
            req.status = 'P'
        try:
            db.session.add(req)
            db.session.commit()
            return True
        except Exception as ex:
            db.session.rollback()
            return False

    def accept_frireq(self, req):
        if req.status != 'P':
            return False
        req.status = 'A'
        try:
            db.session.commit()
            return self.add_friend(req.from_user)
        except Exception as ex:
            traceback.print_exc()
            return False

    def decline_frireq(self, req):
        if req.status != 'P':
            return False
        req.status = 'D'
        try:
            db.session.commit()
            return True
        except Exception as ex:
            traceback.print_exc()
            return False

    def omit_frireq(self, req):
        if req.status != 'P':
            return False
        req.status = 'O'
        try:
            db.session.commit()
            return True
        except Exception as ex:
            traceback.print_exc()
            return False

    def omit_all_frireqs(self):
        reqs = self.recv_frireqs.filter_by(status='P').all()
        for req in reqs:
            req.status = 'O'
        try:
            db.session.add_all(reqs)
            db.session.commit()
            return True
        except Exception as ex:
            traceback.print_exc()
            return False

    def to_dict(self):
        return dict(_id=self._id, uid=self.uid, username=self.username, role=self.role.name)

    def __repr__(self):
        return '<User, uid: {}, username: {}, role: {}>'.format(self.uid, self.username, self.role.name)


class Role(db.Model):
    __tablename__ = 'roles'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'UTF8MB4'}

    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(128))
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role, name: {}, users: {}>'.format(self.name, self.users.count())


class Schedule(db.Model):
    """Model of the schedules"""
    __tablename__ = 'schedules'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'UTF8MB4'}

    _id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.Integer, unique=True, nullable=False, index=True,
                    default=DataUtils.gen_id('schedules', 'sid'))
    title = db.Column(db.String(32), nullable=False, default='未命名')
    detail = db.Column(db.Text)
    sdate = db.Column(db.Date, nullable=False, default=datetime.datetime.utcnow().date)
    stime = db.Column(db.Time, default=datetime.datetime.utcnow().time)
    duration = db.Column(db.Interval, default=datetime.timedelta(hours=1))
    repeat = db.Column(db.String(128))
    alerm = db.Column(db.PickleType, nullable=False, default=[])
    privacy = db.Column(db.SmallInteger, nullable=False, default=SchPrivacy.FRIEND)
    owner_uid = db.Column(db.Integer, db.ForeignKey('users.uid'))
    # backref: owner
    owner_slid = db.Column(db.Integer, db.ForeignKey('schlists.slid'))
    # backref: owner_list

    def to_json(self):
        return {'title': self.title, 'sdate': self.sdate.isoformat()}


class Schlist(db.Model):
    """Model of the schedule lists"""
    __tablename__ = 'schlists'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'UTF8MB4'}

    _id = db.Column(db.Integer, primary_key=True)
    slid = db.Column(db.Integer, unique=True, nullable=False, index=True,
                     default=DataUtils.gen_id('schlists', 'slid'))
    create_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    update_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow,
                          onupdate=datetime.datetime.utcnow)
    closed = db.Column(db.Boolean, nullable=False, default=False)

    # OvM
    owner_uid = db.Column(db.Integer, db.ForeignKey('users.uid'))
    # MvO
    schedules = db.relationship('Schedule', backref='owner_list', lazy='dynamic')
    # MvM
    members = db.relationship('UserSchlist',
                              foreign_keys=[UserSchlist.slid],
                              backref=db.backref('schlist', lazy='joined'),
                              lazy='dynamic',
                              cascade='all, delete-orphan')


_tables = {
    'users': User,
    'roles': Role,
    'schedules': Schedule,
    'schlists': Schlist,
    'friendships': Friendship,
    'user_schlists': UserSchlist,
    'friendreqs': FriendReq
}
