from app import createApp
from backend.models import db, user_datastore

app, _ = createApp()

#this file is for delete the database and create the new one with the default admin and user

def create_empty_tables():
    db.drop_all()
    db.create_all()

with app.app_context():
    create_empty_tables()
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='user', description='user')
    db.session.commit()

    if not user_datastore.find_user(email="admin@spoc.com"):
        admin_user=user_datastore.create_user(email="admin@spoc.com", password="admin")
        user_datastore.add_role_to_user(admin_user, "admin")

    if not user_datastore.find_user(email="user@spoc.com"):
        admin_user=user_datastore.create_user(email="user@spoc.com", password="user")
        user_datastore.add_role_to_user(admin_user, "user")

    db.session.commit()
        