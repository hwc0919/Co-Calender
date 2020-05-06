from flask import render_template, request, session, jsonify

from ..models import *
from .. import db
from . import auth


@auth.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User(username=username, password=password)
    if User.add_user(user):
        return jsonify(dict(success=True, message="注册成功", data=dict(uid=user.uid, username=username)))
    else:
        return jsonify(dict(success=False, message="注册失败"))


@auth.route('/login', methods=['POST'])
def login():
    print(request.json)
    username = request.json.get('username')
    password = request.json.get('password')
    print('username, password:', username, password)
    user = User.query.filter_by(username=username).first()
    print(user)
    if not username or not user or not user.verify_password(password):
        return jsonify(dict(success=False, message="用户名或密码错误"))

    session['login'] = True
    session['username'] = username
    session['uid'] = user.uid
    session.permanent = True
    return jsonify(dict(success=True, message="登录成功", data=dict(uid=user.uid, username=username)))


@auth.route('/test', methods=['GET', 'POST'])
def test():
    if session.get('login'):
        return jsonify(dict(success=True, message='Already login'))
    return jsonify(dict(success=False, message='Fail'))
