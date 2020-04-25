import os

from flask_migrate import Migrate

from app import create_app, db
from app.models import *


app = create_app(os.getenv('FLASK_CONFIG') or 'development')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role,
                Schedule=Schedule, Schlist=Schlist, Friendship=Friendship)


@app.cli.command('resetdb')
def reset_db():
    c = input('ARE YOU SURE (y/N)?')
    if c in ('y', 'Y'):
        db.drop_all()
        db.create_all()
        print('Reset')
    else:
        print('Cancelled')


@app.cli.command('addtest')
def add_test_data():
    entries = []
    super_role = Role(name='Super')
    admin_role = Role(name='Admin')
    user_role = Role(name='User')
    super_user = User(uid=0, username='super', password='super', role=super_role)
    admin_user = User(uid=1, username='admin', password='admin', role=admin_role)
    user_user = User(uid=2, username='user', password='user', role=user_role)
    db.session.add_all([super_role, admin_role, user_role, super_user, admin_user, user_user])

    users = [User(username='user{}'.format(i), password='1234') for i in range(1, 51)]
    db.session.add_all(users)
    db.session.commit()
    print('Add roles and users.')

    import random

    for i in range(50):
        u1 = random.choice(users)
        u2 = random.choice(users)
        if not u1.has_friend(u2):
            u1.add_friend(u2)
    print('Add friends.')
