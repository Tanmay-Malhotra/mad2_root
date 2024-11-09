from app import createApp
from backend.models import db, user_datastore, SponsorProfile, InfluencerProfile

app, _ = createApp()

# This file is for deleting the database and creating a new one with default admin, sponsor, and influencer users.

def create_empty_tables():
    db.drop_all()
    db.create_all()

with app.app_context():
    # Create empty tables
    create_empty_tables()
    
    # Create roles if they don't exist
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='influencer', description='Influencer User')
    user_datastore.find_or_create_role(name='sponsor', description='Sponsor User')
    db.session.commit()

    # Create admin user if it doesn't exist
    if not user_datastore.find_user(email="admin@spoc.com"):
        admin_user = user_datastore.create_user(
            email="admin@spoc.com",
            password="admin",  # Plain text password
            user_type="admin"  # Specify user type as 'admin'
        )
        user_datastore.add_role_to_user(admin_user, "admin")

    # Optionally, create a sample influencer user if it doesn't exist
    if not user_datastore.find_user(email="influencer@spoc.com"):
        influencer_user = user_datastore.create_user(
            email="influencer@spoc.com",
            password="influencer123",  # Plain text password
            user_type="influencer"
        )
        user_datastore.add_role_to_user(influencer_user, "influencer")
        
        # Create and link InfluencerProfile
        influencer_profile = InfluencerProfile(
            user_id=influencer_user.id,
            name="Sample Influencer",
            industry="Technology",
            platform="Instagram",
            followers=5000
        )
        db.session.add(influencer_profile)

    # Optionally, create a sample sponsor user if it doesn't exist
    if not user_datastore.find_user(email="sponsor@spoc.com"):
        sponsor_user = user_datastore.create_user(
            email="sponsor@spoc.com",
            password="sponsor123",  # Plain text password
            user_type="sponsor"
        )
        user_datastore.add_role_to_user(sponsor_user, "sponsor")
        
        # Create and link SponsorProfile
        sponsor_profile = SponsorProfile(
            user_id=sponsor_user.id,
            name="Sample Sponsor",
            industry="Retail"
        )
        db.session.add(sponsor_profile)

    db.session.commit()
