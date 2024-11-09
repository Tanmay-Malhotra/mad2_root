from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from flask_security.datastore import SQLAlchemyUserDatastore

db = SQLAlchemy()



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    # name meine add kiya hai 
    # name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)
    # flask-security specific
    fs_uniquifier = db.Column(db.String, unique = True, nullable = False)
    active = db.Column(db.Boolean, default = True)
    roles = db.Relationship('Role', backref = 'bearers', secondary='user_roles')

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, unique = True, nullable  = False)
    description = db.Column(db.String, nullable = False)

class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

class sponsor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    industry = db.Column(db.String(100))
    flagged = db.Column(db.String(10), nullable=False, default="no")  
    campaigns = db.relationship('campaign', backref='sponsor', lazy=True)

class campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False,default="active")
    category = db.Column(db.String(50), nullable=False)  
    budget = db.Column(db.Integer, nullable=False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id'), nullable=False)
    flagged = db.Column(db.String(10), nullable=False, default="no")
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    
    ad_requests = db.relationship('adrequest', backref='campaign', lazy=True)

class influencer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(100),nullable = False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    platform = db.Column(db.String(100))
    flagged = db.Column(db.String(10), nullable=False, default="no")
    followers = db.Column(db.Integer, nullable=False)
    ad_requests = db.relationship('adrequest', backref='influencer', lazy=True)

class adrequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id'), nullable=False)
    requirements = db.Column(db.String(500), nullable=False)
    flagged = db.Column(db.String(10), nullable=False, default="no")
    payment_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Request Sent')































