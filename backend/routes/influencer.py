#API for influencers to be able to manage adrequests 
from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_security import auth_token_required, current_user
from backend.models import db, AdRequest

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
