from flask import render_template, jsonify, request, session

from ..models import *
from .. import db
from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', message='Welcome to your Flask App')


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
