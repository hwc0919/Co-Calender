from flask import render_template, jsonify, request, session

from ..models import *
from .. import db
from . import main


@main.route('/<name>', methods=['GET', 'POST'])
def index(name):
    return render_template('index.html', message='Welcome to your Flask App, {}'.format(name))


@main.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    uid = data.get('uid', None)
    print('uid:', uid)
    if not uid:
        return jsonify(dict(success=False, message='用户未登录'))
    schedule = Schedule(title=data['title'], owner_uid=uid)
    db.session.add(schedule)
    db.session.commit()
    return jsonify(dict(success=True, data=None))


@main.route('/get-schedules', methods=['GET', 'POST'])
def get_schedules():
    data = request.get_json()
    uid = data.get('uid', None)
    user = User.query.filter_by(uid=uid).first()
    if not uid or not user:
        return jsonify(dict(success=False, message='尚未登录'))
    schedules = [s.to_json() for s in user.schedules.all()]
    return jsonify(dict(success=True, data=schedules))
