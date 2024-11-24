from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_security import auth_token_required, current_user
from backend.models import db, AdRequest, InfluencerProfile, Campaign

class FindInfluencers(Resource):
    @auth_token_required
    def get(self):
        selected_industry = request.args.get('industry', None)
        search_query = request.args.get('search', None)

        query = InfluencerProfile.query

        if selected_industry:
            query = query.filter_by(industry=selected_industry)

        if search_query:
            search_filter = (
                InfluencerProfile.name.ilike(f'%{search_query}%') |
                InfluencerProfile.platform.ilike(f'%{search_query}%')
            )
            query = query.filter(search_filter)

        influencers = query.all()

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


class AcceptNegotiatedAdRequest(Resource):
    @auth_token_required
    def put(self, ad_request_id):
        ad_request = AdRequest.query.get(ad_request_id)
        
        if not ad_request:
            return make_response(jsonify({"error": "Ad request not found"}), 404)

        campaign = Campaign.query.get(ad_request.campaign_id)
        if campaign.sponsor_profile.user_id != current_user.id:
            return make_response(jsonify({"error": "User not authorized to accept this ad request"}), 403)

        if ad_request.status != "Request Negotiated":
            return make_response(jsonify({"error": "Only negotiated requests can be accepted"}), 400)

        ad_request.status = "Request Accepted"
        db.session.commit()

        return make_response(jsonify({"message": "Ad request accepted successfully!"}), 200)

class RejectNegotiatedAdRequest(Resource):
    @auth_token_required
    def put(self, ad_request_id):
        ad_request = AdRequest.query.get(ad_request_id)
        
        if not ad_request:
            return make_response(jsonify({"error": "Ad request not found"}), 404)

        campaign = Campaign.query.get(ad_request.campaign_id)
        if campaign.sponsor_profile.user_id != current_user.id:
            return make_response(jsonify({"error": "User not authorized to reject this ad request"}), 403)

        if ad_request.status != "Request Negotiated":
            return make_response(jsonify({"error": "Only negotiated requests can be rejected"}), 400)

        ad_request.status = "Request Rejected"
        db.session.commit()

        return make_response(jsonify({"message": "Ad request rejected successfully!"}), 200)

class AcceptInfluencerAdRequest(Resource):
    @auth_token_required
    def put(self, ad_request_id):
        ad_request = AdRequest.query.get(ad_request_id)

        if not ad_request:
            return make_response(jsonify({"error": "Ad request not found"}), 404)

        campaign = Campaign.query.get(ad_request.campaign_id)

        if not campaign or campaign.sponsor_profile.user_id != current_user.id:
            return make_response(jsonify({"error": "User not authorized to accept this ad request"}), 403)

        if ad_request.status != "Request Sent by Influencer":
            return make_response(jsonify({"error": "Only ad requests sent by influencers can be accepted"}), 400)

        ad_request.status = "Request Accepted"
        db.session.commit()

        return make_response(jsonify({"message": "Ad request accepted successfully!"}), 200)

class RejectInfluencerAdRequest(Resource):
    @auth_token_required
    def put(self, ad_request_id):
        ad_request = AdRequest.query.get(ad_request_id)

        if not ad_request:
            return make_response(jsonify({"error": "Ad request not found"}), 404)

        campaign = Campaign.query.get(ad_request.campaign_id)

        if not campaign or campaign.sponsor_profile.user_id != current_user.id:
            return make_response(jsonify({"error": "User not authorized to reject this ad request"}), 403)

        if ad_request.status != "Request Sent by Influencer":
            return make_response(jsonify({"error": "Only ad requests sent by influencers can be rejected"}), 400)

        ad_request.status = "Request Rejected"
        db.session.commit()

        return make_response(jsonify({"message": "Ad request rejected successfully!"}), 200)
