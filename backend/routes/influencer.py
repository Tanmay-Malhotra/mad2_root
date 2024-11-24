from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_security import auth_token_required, current_user
from backend.models import db, AdRequest, InfluencerProfile, Campaign


class InfluencerAdRequestList(Resource):
    @auth_token_required
    def get(self, influencer_id):
        
        influencer_profile = InfluencerProfile.query.filter_by(id=influencer_id, user_id=current_user.id).first()
        if not influencer_profile:
            return make_response(jsonify({"error": "Unauthorized access or influencer profile not found"}), 403)

        
        ad_requests = AdRequest.query.filter_by(influencer_profile_id=influencer_id).all()
        

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
        
        ad_request = AdRequest.query.get(ad_request_id)
        
        if not ad_request:
            return make_response(jsonify({"error": "Ad request not found"}), 404)

        if ad_request.influencer_profile_id != current_user.influencer_profile.id:
            return make_response(jsonify({"error": "User not authorized to accept this ad request"}), 403)

        if ad_request.status != "Request Sent":
            return make_response(jsonify({"error": "Only pending ad requests can be accepted"}), 400)

        ad_request.status = "Request Accepted"
        db.session.commit()

        return make_response(jsonify({"message": "Ad request accepted successfully!"}), 200)


class RejectAdRequest(Resource):
    @auth_token_required
    def put(self, ad_request_id):
        
        ad_request = AdRequest.query.get(ad_request_id)
        
        if not ad_request:
            return make_response(jsonify({"error": "Ad request not found"}), 404)

        if ad_request.influencer_profile_id != current_user.influencer_profile.id:
            return make_response(jsonify({"error": "User not authorized to reject this ad request"}), 403)

        if ad_request.status != "Request Sent":
            return make_response(jsonify({"error": "Only pending ad requests can be rejected"}), 400)

        ad_request.status = "Request Rejected"
        db.session.commit()

        return make_response(jsonify({"message": "Ad request rejected successfully!"}), 200)



class NegotiateAdRequest(Resource):
    @auth_token_required
    def put(self, ad_request_id):

        ad_request = AdRequest.query.get(ad_request_id)
        

        if not ad_request:
            return make_response(jsonify({"error": "Ad request not found"}), 404)


        if ad_request.influencer_profile_id != current_user.influencer_profile.id:
            return make_response(jsonify({"error": "User not authorized to negotiate this ad request"}), 403)

        data = request.get_json()
        requirements = data.get('requirements')
        payment_amount = data.get('payment_amount')

        if requirements is not None:
            ad_request.requirements = requirements
        if payment_amount is not None:
            try:
                ad_request.payment_amount = float(payment_amount)
            except ValueError:
                return make_response(jsonify({"error": "Invalid payment amount"}), 400)

        ad_request.status = "Request Negotiated"
        
        db.session.commit()

        return make_response(jsonify({"message": "Ad request has been negotiated and sent back to sponsor for review"}), 200)


class PublicCampaignList(Resource):
    @auth_token_required
    def get(self, influencer_id):
        influencer_profile = InfluencerProfile.query.filter_by(id=influencer_id, user_id=current_user.id).first()

        public_campaigns = Campaign.query.filter_by(type="public", status="active").all()

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

        campaign = Campaign.query.get(campaign_id)
        if not campaign or campaign.type != 'public':
            return make_response(jsonify({"error": "Campaign not found or not public"}), 404)

        influencer_profile = InfluencerProfile.query.filter_by(user_id=current_user.id).first()
        if not influencer_profile:
            return make_response(jsonify({"error": "User is not an influencer"}), 403)

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


class InfluencerEditProfile(Resource):
    @auth_token_required
    def put(self):
        data = request.get_json()
        new_name = data.get('name')
        new_followers = data.get('followers')

        if not new_name or not isinstance(new_name, str):
            return make_response(jsonify({"error": "Invalid or missing 'name' field"}), 400)
        if not isinstance(new_followers, int) or new_followers <= 0:
            return make_response(jsonify({"error": "Invalid 'followers' count"}), 400)

        influencer_profile = InfluencerProfile.query.filter_by(user_id=current_user.id).first()
        if not influencer_profile:
            return make_response(jsonify({"error": "User is not an influencer"}), 403)

        influencer_profile.name = new_name
        influencer_profile.followers = new_followers

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
