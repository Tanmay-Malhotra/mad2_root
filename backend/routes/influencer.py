#API for influencers to be able to manage adrequests 
from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_security import auth_token_required, current_user
from backend.models import db, AdRequest

from flask import jsonify, make_response
from flask_restful import Resource
from flask_security import auth_token_required, current_user
from backend.models import AdRequest, InfluencerProfile

class InfluencerAdRequestList(Resource):
    @auth_token_required
    def get(self, influencer_id):
        # Verify that the current user is the owner of this profile
        influencer_profile = InfluencerProfile.query.filter_by(id=influencer_id, user_id=current_user.id).first()
        if not influencer_profile:
            return make_response(jsonify({"error": "Unauthorized access or influencer profile not found"}), 403)

        # Fetch ad requests related to this influencer
        ad_requests = AdRequest.query.filter_by(influencer_profile_id=influencer_id).all()
        
        # Serialize ad request data
        ad_requests_data = [
            {
                "id": ad_request.id,
                "campaign_name": ad_request.campaign.name,
                "requirements": ad_request.requirements,
                "payment_amount": ad_request.payment_amount,
                "status": ad_request.status
            }
            for ad_request in ad_requests
        ]

        return make_response(jsonify({"ad_requests": ad_requests_data}), 200)


class AcceptAdRequest(Resource):
    @auth_token_required
    def put(self, ad_request_id):
        # Get the ad request by ad_request_id
        ad_request = AdRequest.query.get(ad_request_id)
        
        # Verify if the ad request exists
        if not ad_request:
            return make_response(jsonify({"error": "Ad request not found"}), 404)

        # Check if the current user is the influencer for this ad request
        if ad_request.influencer_profile_id != current_user.influencer_profile.id:
            return make_response(jsonify({"error": "User not authorized to accept this ad request"}), 403)

        # Check if the ad request status is "Request Sent"
        if ad_request.status != "Request Sent":
            return make_response(jsonify({"error": "Only pending ad requests can be accepted"}), 400)

        # Update the status to "Request Accepted"
        ad_request.status = "Request Accepted"
        db.session.commit()

        return make_response(jsonify({"message": "Ad request accepted successfully!"}), 200)


class RejectAdRequest(Resource):
    @auth_token_required
    def put(self, ad_request_id):
        # Get the ad request by ad_request_id
        ad_request = AdRequest.query.get(ad_request_id)
        
        # Verify if the ad request exists
        if not ad_request:
            return make_response(jsonify({"error": "Ad request not found"}), 404)

        # Check if the current user is the influencer for this ad request
        if ad_request.influencer_profile_id != current_user.influencer_profile.id:
            return make_response(jsonify({"error": "User not authorized to reject this ad request"}), 403)

        # Check if the ad request status is "Request Sent"
        if ad_request.status != "Request Sent":
            return make_response(jsonify({"error": "Only pending ad requests can be rejected"}), 400)

        # Update the status to "Request Rejected"
        ad_request.status = "Request Rejected"
        db.session.commit()

        return make_response(jsonify({"message": "Ad request rejected successfully!"}), 200)

from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_security import auth_token_required, current_user
from backend.models import db, AdRequest

class NegotiateAdRequest(Resource):
    @auth_token_required
    def put(self, ad_request_id):
        # Get the ad request by ad_request_id
        ad_request = AdRequest.query.get(ad_request_id)
        
        # Verify if the ad request exists
        if not ad_request:
            return make_response(jsonify({"error": "Ad request not found"}), 404)

        # Check if the current user is the influencer for this ad request
        if ad_request.influencer_profile_id != current_user.influencer_profile.id:
            return make_response(jsonify({"error": "User not authorized to negotiate this ad request"}), 403)

        # Parse data from the JSON request
        data = request.get_json()
        requirements = data.get('requirements')
        payment_amount = data.get('payment_amount')

        # Update the fields for negotiation if they are provided
        if requirements is not None:
            ad_request.requirements = requirements
        if payment_amount is not None:
            try:
                ad_request.payment_amount = float(payment_amount)
            except ValueError:
                return make_response(jsonify({"error": "Invalid payment amount"}), 400)

        # Set the status to "Request Negotiated" to indicate that the influencer has updated the request
        ad_request.status = "Request Negotiated"
        
        # Commit the changes to the database
        db.session.commit()

        return make_response(jsonify({"message": "Ad request has been negotiated and sent back to sponsor for review"}), 200)

# create a method for influencers to find campaigns

from flask import jsonify, make_response
from flask_restful import Resource
from flask_security import auth_token_required, current_user
from backend.models import Campaign, InfluencerProfile

class PublicCampaignList(Resource):
    @auth_token_required
    def get(self, influencer_id):
        # Verify that the current user is the owner of this influencer profile
        influencer_profile = InfluencerProfile.query.filter_by(id=influencer_id, user_id=current_user.id).first()
    
            # Fetch public campaigns
        public_campaigns = Campaign.query.filter_by(type="public", status="active").all()

        # Serialize campaign data
        campaigns_data = [
            {
                "id": campaign.id,
                "name": campaign.name,
                "category": campaign.category,
                "budget": campaign.budget,
                "start_date": campaign.start_date.strftime('%Y-%m-%d'),
                "end_date": campaign.end_date.strftime('%Y-%m-%d') if campaign.end_date else None,
                "sponsor_name": campaign.sponsor_profile.name
            }
            for campaign in public_campaigns
        ]

        return make_response(jsonify({"public_campaigns": campaigns_data}), 200)
    
class InfluencerInitiateAdRequest(Resource):
    @auth_token_required
    def post(self, campaign_id):
        data = request.get_json()
        requirements = data.get('requirements')
        payment_amount = data.get('payment_amount')

        # Verify if the campaign exists
        campaign = Campaign.query.get(campaign_id)
        if not campaign or campaign.type != 'public':
            return make_response(jsonify({"error": "Campaign not found or not public"}), 404)

        # Verify if the current user is an influencer
        influencer_profile = InfluencerProfile.query.filter_by(user_id=current_user.id).first()
        if not influencer_profile:
            return make_response(jsonify({"error": "User is not an influencer"}), 403)

        # Create a new ad request with the status "Request Initiated by Influencer"
        new_ad_request = AdRequest(
            campaign_id=campaign_id,
            influencer_profile_id=influencer_profile.id,
            requirements=requirements,
            payment_amount=float(payment_amount),
            status='Request Sent by Influencer'
        )

        db.session.add(new_ad_request)
        db.session.commit()

        return make_response(jsonify({"message": "Ad request sent to sponsor successfully!"}), 201)

from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_security import auth_token_required, current_user
from backend.models import db, InfluencerProfile

class InfluencerEditProfile(Resource):
    @auth_token_required
    def put(self):
        # Parse JSON request data
        data = request.get_json()
        new_name = data.get('name')
        new_followers = data.get('followers')

        # Validate input
        if not new_name or not isinstance(new_name, str):
            return make_response(jsonify({"error": "Invalid or missing 'name' field"}), 400)
        if not isinstance(new_followers, int) or new_followers <= 0:
            return make_response(jsonify({"error": "Invalid 'followers' count"}), 400)

        # Retrieve influencer profile for the current user
        influencer_profile = InfluencerProfile.query.filter_by(user_id=current_user.id).first()
        if not influencer_profile:
            return make_response(jsonify({"error": "User is not an influencer"}), 403)

        # Update profile details
        influencer_profile.name = new_name
        influencer_profile.followers = new_followers

        # Commit changes to the database
        try:
            db.session.commit()
            return make_response(jsonify({
                "message": "Profile updated successfully",
                "name": influencer_profile.name,
                "followers": influencer_profile.followers
            }), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": f"Database error: {str(e)}"}), 500)
