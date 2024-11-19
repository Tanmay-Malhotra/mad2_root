from flask import Flask, jsonify
from flask_security import Security, SQLAlchemyUserDatastore, auth_required
from flask_restful import Api
from flask_cors import CORS
from backend.models import db, User, Role  # Ensure these imports are correct
from backend.routes.auth import Signin, InfluencerSignup, SponsorSignup
from worker import celery_init_app
from celery.schedules import crontab
from task import monthly_reminder,daily_reminder
from mail_config import Config

def createApp():
    app = Flask(__name__)
    
    # Load configuration
    from config import LocalDevelopmentConfig
    app.config.from_object(LocalDevelopmentConfig)
    app.config.from_object(Config)
    # Initialize database
    db.init_app(app)
    
    # Set up Flask-Security with SQLAlchemyUserDatastore
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore, register_blueprint=False)

    # Initialize API and CORS
    api = Api(app)
    CORS(app)

    return app, api



# Create the app and API handler
app, api_handler = createApp()
celery_app = celery_init_app(app)

@celery_app.on_after_configure.connect
def celery_job(sender, **kwargs):
    # sender.add_periodic_task(crontab(hour=8, minute=0, day_of_month=1), monthly_reminder.s())
    # sender.add_periodic_task(crontab(hour=18, minute=0), daily_reminder.s())

    # for testing
    sender.add_periodic_task(60, monthly_reminder.s())
    sender.add_periodic_task(10, daily_reminder.s())

# Example of a protected route using Flask-Security
@app.get('/protected')
@auth_required()  # Requires authenticated user
def protected():
    return '<h1>Only accessible by authenticated user</h1>'

#----------------API Routes-----------------------------------------------------

# Add resources for API routes
api_handler.add_resource(Signin, "/signin")
api_handler.add_resource(InfluencerSignup, "/signup/influencer")  # Separate endpoint for influencers
api_handler.add_resource(SponsorSignup, "/signup/sponsor")       # Separate endpoint for sponsors



# API for campaign management for sponsor
from backend.routes.campaigns import Campaigns,CreateCampaign,EditCampaign,DeleteCampaign

api_handler.add_resource(Campaigns, "/campaigns/<int:sponsor_id>")
api_handler.add_resource(CreateCampaign, "/sponsor/create_camp")
api_handler.add_resource(EditCampaign, '/edit_campaign/<int:campaign_id>')
api_handler.add_resource(DeleteCampaign, '/delete_campaign/<int:campaign_id>')

# API for adrequest management for sponsor 
from backend.routes.campaigns import CreateAdRequest,ViewAdRequests,UpdateAdRequest,DeleteAdRequest

api_handler.add_resource(CreateAdRequest, '/sponsor/campaign/ad_request/<int:influencer_id>')
api_handler.add_resource(ViewAdRequests, '/sponsor/campaign/<int:campaign_id>/ad_requests')
api_handler.add_resource(UpdateAdRequest, '/campaign/update_ad_request/<int:ad_request_id>')
api_handler.add_resource(DeleteAdRequest, '/campaign/delete_ad_request/<int:ad_request_id>')


#API for sponsor to find influncers 
from backend.routes.sponsor import FindInfluencers,AcceptInfluencerAdRequest,RejectInfluencerAdRequest
api_handler.add_resource(FindInfluencers, '/sponsor/inf_find')
api_handler.add_resource(AcceptInfluencerAdRequest, '/accept_influencer_ad_request/<int:ad_request_id>')
api_handler.add_resource(RejectInfluencerAdRequest, '/reject_influencer_ad_request/<int:ad_request_id>')



#API for influencer to manage add request 
from backend.routes.influencer import AcceptAdRequest,RejectAdRequest,NegotiateAdRequest,InfluencerAdRequestList,PublicCampaignList

api_handler.add_resource(InfluencerAdRequestList, '/influencer/ad_requests/<int:influencer_id>')
api_handler.add_resource(AcceptAdRequest, '/accept_ad_request/<int:ad_request_id>')
api_handler.add_resource(RejectAdRequest, '/reject_ad_request/<int:ad_request_id>')
api_handler.add_resource(NegotiateAdRequest, '/negotiate_ad_request/<int:ad_request_id>')
api_handler.add_resource(PublicCampaignList, '/influencer/public_campaigns/<int:influencer_id>')

from backend.routes.influencer import InfluencerEditProfile
api_handler.add_resource(InfluencerEditProfile, '/edit_influencer_profile')

from backend.routes.influencer import InfluencerInitiateAdRequest
api_handler.add_resource(InfluencerInitiateAdRequest, '/influencer/campaign/ad_request/<int:campaign_id>')

from backend.routes.sponsor import SponsorNegotiateAdRequest, AcceptNegotiatedAdRequest,RejectNegotiatedAdRequest

# not sure if I need this sponsor negotiate ad request ??
api_handler.add_resource(SponsorNegotiateAdRequest,'/sponsor/negotiate_ad_request/<int:ad_request_id>')
api_handler.add_resource(AcceptNegotiatedAdRequest, '/accept_negotiated_ad_request/<int:ad_request_id>')
api_handler.add_resource(RejectNegotiatedAdRequest, '/reject_negotiated_ad_request/<int:ad_request_id>')


#-------admin -------------------
from backend.routes.admin import SponsorsListView,AdminDashboardView,ApproveSponsorView,RejectSponsorView,ToggleFlagSponsorView,ToggleFlagAdRequestView,ToggleFlagCampaignView,ToggleFlagInfluencerView
api_handler.add_resource(AdminDashboardView, '/admin_dashboard')

#sponsor management
api_handler.add_resource(ApproveSponsorView, '/sponsor/approve/<int:sponsor_id>')
api_handler.add_resource(RejectSponsorView, '/sponsor/reject/<int:sponsor_id>')
api_handler.add_resource(ToggleFlagSponsorView, '/sponsor/toggle_flag/<int:sponsor_id>')
api_handler.add_resource(SponsorsListView, '/admin/sponsors')

from backend.routes.admin import AllCampaignsView,AllInfluencersView
api_handler.add_resource(AllCampaignsView, '/admin/campaigns')
api_handler.add_resource(AllInfluencersView, '/admin/influencers')

#Flag
api_handler.add_resource(ToggleFlagInfluencerView, '/influencer/toggle_flag/<int:influencer_id>')
api_handler.add_resource(ToggleFlagCampaignView, '/campaign/toggle_flag/<int:campaign_id>')
api_handler.add_resource(ToggleFlagAdRequestView, '/adrequest/toggle_flag/<int:ad_request_id>')


from backend.routes.admin import AdminDeleteAdRequestView,AdminDeleteCampaignView,AdminDeleteInfluencerView,AdminDeleteSponsorView
api_handler.add_resource(AdminDeleteSponsorView, '/admin/sponsor/delete/<int:sponsor_id>')
api_handler.add_resource(AdminDeleteInfluencerView, '/admin/influencer/delete/<int:influencer_id>')
api_handler.add_resource(AdminDeleteCampaignView, '/admin/campaign/delete/<int:campaign_id>')
api_handler.add_resource(AdminDeleteAdRequestView, '/admin/ad_request/delete/<int:ad_request_id>')


if __name__ == '__main__':
    app.run()
