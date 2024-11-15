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
