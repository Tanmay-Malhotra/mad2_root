from flask import Flask, jsonify
from flask_security import Security, SQLAlchemyUserDatastore, auth_required
from flask_restful import Api
from flask_cors import CORS
from backend.models import db, User, Role  # Ensure these imports are correct
from backend.routes.auth import Signin, InfluencerSignup, SponsorSignup


def createApp():
    app = Flask(__name__)
    
    # Load configuration
    from backend.config import LocalDevelopmentConfig
    app.config.from_object(LocalDevelopmentConfig)
    
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
from backend.routes.sponsor import FindInfluencers
api_handler.add_resource(FindInfluencers, '/sponsor/inf_find')


#API for influencer to manage add request 
from backend.routes.influencer import AcceptAdRequest,RejectAdRequest

api_handler.add_resource(AcceptAdRequest, '/accept_ad_request/<int:ad_request_id>')
api_handler.add_resource(RejectAdRequest, '/reject_ad_request/<int:ad_request_id>')



if __name__ == '__main__':
    app.run()
