#API for sponsor to find influencer 
from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_security import auth_token_required
from backend.models import InfluencerProfile

class FindInfluencers(Resource):
    @auth_token_required
    def get(self):
        # Get optional filter parameters
        selected_industry = request.args.get('industry', None)
        search_query = request.args.get('search', None)

        # Initialize the query
        query = InfluencerProfile.query

        # Filter by industry if provided
        if selected_industry:
            query = query.filter_by(industry=selected_industry)

        # Search influencers by name, username, or email if a search query is provided
        if search_query:
            search_filter = (
                InfluencerProfile.name.ilike(f'%{search_query}%') |
                InfluencerProfile.platform.ilike(f'%{search_query}%')
            )
            query = query.filter(search_filter)

        # Execute the query to get the list of influencers
        influencers = query.all()

        # Convert influencer profiles to a dictionary format for JSON response
        influencers_data = [
            {
                "id": influencer.id,
                "name": influencer.name,
                "industry": influencer.industry,
                "platform": influencer.platform,
                "followers": influencer.followers
            }
            for influencer in influencers
        ]

        return make_response(jsonify({"influencers": influencers_data}), 200)

from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_security import auth_token_required, current_user
from backend.models import db, AdRequest, Campaign

class SponsorNegotiateAdRequest(Resource):
    @auth_token_required
    def put(self, ad_request_id):
        # Get the ad request by ad_request_id
        ad_request = AdRequest.query.get(ad_request_id)
        
        # Verify if the ad request exists
        if not ad_request:
            return make_response(jsonify({"error": "Ad request not found"}), 404)

        # Check if the current user is the sponsor for this ad request
        campaign = Campaign.query.get(ad_request.campaign_id)
        if campaign.sponsor_profile.user_id != current_user.id:
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

        # Set the status to "Request Negotiated" to indicate that the sponsor has modified the request
        ad_request.status = "Request Negotiated"
        
        # Commit the changes to the database
        db.session.commit()

        return make_response(jsonify({"message": "Ad request has been negotiated and sent back to influencer for review"}), 200)

from flask import jsonify, make_response
from flask_restful import Resource
from flask_security import auth_token_required, current_user
from backend.models import db, AdRequest, Campaign

class AcceptNegotiatedAdRequest(Resource):
    @auth_token_required
    def put(self, ad_request_id):
        # Get the ad request by ad_request_id
        ad_request = AdRequest.query.get(ad_request_id)
        
        # Verify if the ad request exists
        if not ad_request:
            return make_response(jsonify({"error": "Ad request not found"}), 404)

        # Check if the current user is the sponsor for this ad request
        campaign = Campaign.query.get(ad_request.campaign_id)
        if campaign.sponsor_profile.user_id != current_user.id:
            return make_response(jsonify({"error": "User not authorized to accept this ad request"}), 403)

        # Check if the ad request status is "Request Negotiated"
        if ad_request.status != "Request Negotiated":
            return make_response(jsonify({"error": "Only negotiated requests can be accepted"}), 400)

        # Update the status to "Request Accepted"
        ad_request.status = "Request Accepted"
        db.session.commit()

        return make_response(jsonify({"message": "Ad request accepted successfully!"}), 200)


class RejectNegotiatedAdRequest(Resource):
    @auth_token_required
    def put(self, ad_request_id):
        # Get the ad request by ad_request_id
        ad_request = AdRequest.query.get(ad_request_id)
        
        # Verify if the ad request exists
        if not ad_request:
            return make_response(jsonify({"error": "Ad request not found"}), 404)

        # Check if the current user is the sponsor for this ad request
        campaign = Campaign.query.get(ad_request.campaign_id)
        if campaign.sponsor_profile.user_id != current_user.id:
            return make_response(jsonify({"error": "User not authorized to reject this ad request"}), 403)

        # Check if the ad request status is "Request Negotiated"
        if ad_request.status != "Request Negotiated":
            return make_response(jsonify({"error": "Only negotiated requests can be rejected"}), 400)

        # Update the status to "Request Rejected"
        ad_request.status = "Request Rejected"
        db.session.commit()

        return make_response(jsonify({"message": "Ad request rejected successfully!"}), 200)
