from flask import current_app as app
from backend.models import db
from flask_security import SQLAlchemyUserDatastore, hash_password

with app.app_context():
    db.create_all()

    userdatastore : SQLAlchemyUserDatastore = app.security.datastore

    userdatastore.find_or_create_role(name = 'admin', description = 'superuser')
    userdatastore.find_or_create_role(name = 'user', description = 'general user')

    if (not userdatastore.find_user(email = 'admin@spoc.in')):
        userdatastore.create_user(name = 'admin', email = 'admin@spoc.in', password = hash_password('pass'), roles = ['admin'] )
    if (not userdatastore.find_user(email = 'user01@spoc.in')):
        userdatastore.create_user(name = 'user01', email = 'user01@spoc.in', password = hash_password('pass'), roles = ['user'] ) # for testing

    db.session.commit()