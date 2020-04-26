from flask import render_template, request

from .. import db
from . import auth


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return 'register page'
    return 'regiter submit'


@auth.route('/login', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return 'login page'
    return 'login submit'
