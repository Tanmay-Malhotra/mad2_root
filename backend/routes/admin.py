from flask import request, jsonify, make_response, session
from flask_restful import Resource
from flask_security import auth_token_required, roles_accepted
from backend.models import db, User, Role, SponsorProfile, InfluencerProfile, Campaign, AdRequest

class AdminDashboardView(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def get(self):
        # Fetch statistics
        total_users = SponsorProfile.query.count() + InfluencerProfile.query.count()
        number_of_sponsors = SponsorProfile.query.count()
        number_of_influencers = InfluencerProfile.query.count()
        number_of_campaigns = Campaign.query.count()
        active_ad_requests = AdRequest.query.filter_by(status='Request Accepted').count()
        flagged_sponsors = SponsorProfile.query.filter_by(flagged='yes').count()
        flagged_influencers = InfluencerProfile.query.filter_by(flagged='yes').count()
        flagged_campaigns = Campaign.query.filter_by(flagged='yes').count()
        flagged_ad_requests = AdRequest.query.filter_by(flagged='yes').count()

        data = {
            'total_users': total_users,
            'number_of_sponsors': number_of_sponsors,
            'number_of_influencers': number_of_influencers,
            'number_of_campaigns': number_of_campaigns,
            'active_ad_requests': active_ad_requests,
            'flagged_sponsors': flagged_sponsors,
            'flagged_influencers': flagged_influencers,
            'flagged_campaigns': flagged_campaigns,
            'flagged_ad_requests': flagged_ad_requests
        }

        return make_response(jsonify(data), 200)

from flask import jsonify, make_response
from flask_restful import Resource
from flask_security import auth_token_required, roles_accepted
from backend.models import db, SponsorProfile

class SponsorsListView(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def get(self):
        # Get all sponsors with their approval status and flag status
        sponsors = SponsorProfile.query.all()
        sponsors_data = [
            {
                "id": sponsor.id,
                "name": sponsor.name,
                "user": {
                    "email": sponsor.user.email  # Assuming there is a relationship between SponsorProfile and User
                },
                "industry": sponsor.industry,
                "flagged": sponsor.flagged,
                "approved": sponsor.approved
            }
            for sponsor in sponsors
        ]
        return jsonify({"sponsors": sponsors_data})

class ApproveSponsorView(Resource):
    @auth_token_required
    @roles_accepted('admin')  # Only admins can approve
    def put(self, sponsor_id):
        sponsor = SponsorProfile.query.get(sponsor_id)
        
        if not sponsor:
            return make_response(jsonify({"message": "Sponsor not found"}), 404)
        
        # Approve the sponsor
        sponsor.approved = True
        db.session.commit()
        
        return make_response(jsonify({"message": "Sponsor account approved successfully"}), 200)

class RejectSponsorView(Resource):
    @auth_token_required
    @roles_accepted('admin')  # Only admins can reject
    def put(self, sponsor_id):
        sponsor = SponsorProfile.query.get(sponsor_id)
        
        if not sponsor:
            return make_response(jsonify({"message": "Sponsor not found"}), 404)
        
        # Reject the sponsor
        sponsor.approved = False
        db.session.commit()
        
        return make_response(jsonify({"message": "Sponsor account rejected successfully"}), 200)
    
from flask import jsonify, make_response
from flask_restful import Resource
from flask_security import auth_token_required, roles_accepted
from backend.models import db, SponsorProfile

class ToggleFlagSponsorView(Resource):
    @auth_token_required
    @roles_accepted('admin')  # Only admins can toggle the flagged status
    def put(self, sponsor_id):
        sponsor = SponsorProfile.query.get(sponsor_id)
        
        if not sponsor:
            return make_response(jsonify({"message": "Sponsor not found"}), 404)
        
        # Toggle the flagged status
        sponsor.flagged = "no" if sponsor.flagged == "yes" else "yes"
        db.session.commit()
        
        return make_response(jsonify({
            "message": "Sponsor flagged status updated successfully",
            "sponsor_id": sponsor_id,
            "new_flagged_status": sponsor.flagged
        }), 200)

from flask import jsonify, make_response
from flask_restful import Resource
from flask_security import auth_token_required, roles_accepted
from backend.models import db, InfluencerProfile, Campaign, AdRequest

class ToggleFlagInfluencerView(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def put(self, influencer_id):
        influencer = InfluencerProfile.query.get(influencer_id)
        
        if not influencer:
            return make_response(jsonify({"message": "Influencer not found"}), 404)
        
        # Toggle the flagged status
        influencer.flagged = "no" if influencer.flagged == "yes" else "yes"
        db.session.commit()
        
        return make_response(jsonify({
            "message": "Influencer flagged status updated successfully",
            "influencer_id": influencer_id,
            "new_flagged_status": influencer.flagged
        }), 200)

class ToggleFlagCampaignView(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def put(self, campaign_id):
        campaign = Campaign.query.get(campaign_id)
        
        if not campaign:
            return make_response(jsonify({"message": "Campaign not found"}), 404)
        
        # Toggle the flagged status
        campaign.flagged = "no" if campaign.flagged == "yes" else "yes"
        db.session.commit()
        
        return make_response(jsonify({
            "message": "Campaign flagged status updated successfully",
            "campaign_id": campaign_id,
            "new_flagged_status": campaign.flagged
        }), 200)

class ToggleFlagAdRequestView(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def put(self, ad_request_id):
        ad_request = AdRequest.query.get(ad_request_id)
        
        if not ad_request:
            return make_response(jsonify({"message": "Ad Request not found"}), 404)
        
        # Toggle the flagged status
        ad_request.flagged = "no" if ad_request.flagged == "yes" else "yes"
        db.session.commit()
        
        return make_response(jsonify({
            "message": "Ad Request flagged status updated successfully",
            "ad_request_id": ad_request_id,
            "new_flagged_status": ad_request.flagged
        }), 200)
    
class AdminDeleteSponsorView(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def delete(self, sponsor_id):


        sponsor = SponsorProfile.query.get(sponsor_id)

        # Delete associated ad requests through campaigns
        ad_requests = AdRequest.query.join(Campaign).filter(Campaign.sponsor_profile_id == sponsor_id).all()
        for ad_request in ad_requests:
            db.session.delete(ad_request)

        # Delete associated campaigns
        campaigns = Campaign.query.filter_by(sponsor_profile_id=sponsor_id).all()
        for campaign in campaigns:
            db.session.delete(campaign)

        # Delete the sponsor profile
        db.session.delete(sponsor)
        db.session.commit()
        return make_response(jsonify({"message": "Sponsor and all associated data have been deleted."}), 200)
    
class AdminDeleteInfluencerView(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def delete(self, influencer_id):


        influencer = InfluencerProfile.query.get(influencer_id)
        if not influencer:
            return make_response(jsonify({"message": "Influencer not found"}), 404)

        # Delete associated ad requests
        ad_requests = AdRequest.query.filter_by(influencer_profile_id=influencer_id).all()
        for ad_request in ad_requests:
            db.session.delete(ad_request)

        # Delete the influencer profile
        db.session.delete(influencer)
        db.session.commit()
        return make_response(jsonify({"message": "Influencer and their associated ad requests have been deleted."}), 200)

class AdminDeleteCampaignView(Resource):
    def delete(self, campaign_id):


        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return make_response(jsonify({"message": "Campaign not found"}), 404)

        # Delete associated ad requests
        ad_requests = AdRequest.query.filter_by(campaign_id=campaign_id).all()
        for ad_request in ad_requests:
            db.session.delete(ad_request)

        # Delete the campaign
        db.session.delete(campaign)
        db.session.commit()
        return make_response(jsonify({"message": "Campaign and all associated data have been deleted."}), 200)
    
class AdminDeleteAdRequestView(Resource):
    def delete(self, ad_request_id):


        ad_request = AdRequest.query.get(ad_request_id)
        if not ad_request:
            return make_response(jsonify({"message": "Ad request not found"}), 404)

        db.session.delete(ad_request)
        db.session.commit()
        return make_response(jsonify({"message": "Ad request has been deleted."}), 200)