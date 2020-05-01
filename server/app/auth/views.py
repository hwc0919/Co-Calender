from flask import render_template, request, session, jsonify

from ..models import *
from .. import db
from . import auth


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return 'register page'
    return 'regiter submit'


@auth.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if not username or not user or not user.verify_password(password):
        return jsonify(dict(success=False, message="登录失败"))

    return jsonify(dict(success=True, message="登录成功", username=username))
