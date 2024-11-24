from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore


db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    fs_uniquifier = db.Column(db.String, unique=True, nullable=False)
    active = db.Column(db.Boolean, default=True)
    roles = db.relationship('Role', backref='bearers', secondary='user_roles')

    user_type = db.Column(db.String(20), nullable=False)  

    sponsor_profile = db.relationship('SponsorProfile', uselist=False, backref='user')
    influencer_profile = db.relationship('InfluencerProfile', uselist=False, backref='user')

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)

class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

class SponsorProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    name = db.Column(db.String(100), nullable=True)
    industry = db.Column(db.String(100))
    flagged = db.Column(db.String(10), nullable=False, default="no")
    approved = db.Column(db.Boolean, default=False)
    
    campaigns = db.relationship('Campaign', backref='sponsor_profile', lazy=True)

class InfluencerProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    name = db.Column(db.String(100), nullable=True)
    industry = db.Column(db.String(100), nullable=False)
    platform = db.Column(db.String(100))
    flagged = db.Column(db.String(10), nullable=False, default="no")
    followers = db.Column(db.Integer, nullable=False)

    ad_requests = db.relationship('AdRequest', backref='influencer_profile', lazy=True)

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="active")
    category = db.Column(db.String(50), nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    sponsor_profile_id = db.Column(db.Integer, db.ForeignKey('sponsor_profile.id'), nullable=False)
    flagged = db.Column(db.String(10), nullable=False, default="no")
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)

    type = db.Column(db.String(10), nullable=False, default="private")

    ad_requests = db.relationship('AdRequest', backref='campaign', lazy=True)

class AdRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    influencer_profile_id = db.Column(db.Integer, db.ForeignKey('influencer_profile.id'), nullable=False)
    requirements = db.Column(db.String(500), nullable=False)
    flagged = db.Column(db.String(10), nullable=False, default="no")
    payment_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Request Sent')
    