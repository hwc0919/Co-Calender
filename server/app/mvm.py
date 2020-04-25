import datetime

from . import db


class Friendship(db.Model):
    __tablename__ = 'friendships'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'UTF8MB4'}

    from_uid = db.Column(db.Integer, db.ForeignKey('users.uid'), primary_key=True)
    to_uid = db.Column(db.Integer, db.ForeignKey('users.uid'), primary_key=True)
    group = db.Column(db.String(16), nullable=False, default='默认分组')
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class UserSchlist(db.Model):
    __tablename__ = 'user_schlists'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'UTF8MB4'}

    uid = db.Column(db.Integer, db.ForeignKey('users.uid'), primary_key=True)
    slid = db.Column(db.Integer, db.ForeignKey('schlists.slid'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
