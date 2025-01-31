from app import createApp
from backend.models import db, user_datastore, SponsorProfile, InfluencerProfile, Campaign, AdRequest
from datetime import date

app, _ = createApp()


def create_empty_tables():
    db.drop_all()
    db.create_all()

with app.app_context():
    
    create_empty_tables()
    
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='influencer', description='Influencer User')
    user_datastore.find_or_create_role(name='sponsor', description='Sponsor User')
    db.session.commit()

    if not user_datastore.find_user(email="admin@spoc.com"):
        admin_user = user_datastore.create_user(
            email="admin@spoc.com",
            password="admin", 
            user_type="admin"  
        )
        user_datastore.add_role_to_user(admin_user, "admin")


    if not user_datastore.find_user(email="influencer@spoc.com"):
        influencer_user = user_datastore.create_user(
            email="influencer@spoc.com",
            password="pass", 
            user_type="influencer"
        )
        user_datastore.add_role_to_user(influencer_user, "influencer")
        
        influencer_profile = InfluencerProfile(
            user_id=influencer_user.id,
            name="Sample Influencer",
            industry="Technology",
            platform="Instagram",
            followers=5000
        )
        db.session.add(influencer_profile)


    if not user_datastore.find_user(email="sponsor@spoc.com"):
        sponsor_user = user_datastore.create_user(
            email="sponsor@spoc.com",
            password="pass",  
            user_type="sponsor"
        )
        user_datastore.add_role_to_user(sponsor_user, "sponsor")
        

        sponsor_profile = SponsorProfile(
            user_id=sponsor_user.id,
            name="Sample Sponsor",
            industry="Retail"
        )
        db.session.add(sponsor_profile)
        db.session.commit() 

  
        campaign = Campaign(
            name="Sample Campaign",
            status="active",
            category="Marketing",
            budget=10000,
            sponsor_profile_id=sponsor_profile.id,
            flagged="no",
            start_date=date.today(),
            end_date=None  
        )
        db.session.add(campaign)
        db.session.commit()  

        ad_request = AdRequest(
            campaign_id=campaign.id,
            influencer_profile_id=influencer_profile.id,
            requirements="Create a social media post promoting the campaign",
            flagged="no",
            payment_amount=500.0,
            status="Request Accepted"  # Mark the request as accepted by default
        )
        db.session.add(ad_request)

    db.session.commit()
