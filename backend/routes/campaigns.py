from flask import request, session, jsonify, make_response
from flask_restful import Resource
from flask_security import auth_token_required, current_user
from datetime import date
from backend.models import db, Campaign, SponsorProfile, User, AdRequest, InfluencerProfile

class Campaigns(Resource):
    @auth_token_required  
    def get(self, sponsor_id):
        if not sponsor_id:
            return make_response(jsonify({"error": "Sponsor ID is required"}), 400)

        sponsor_profile = SponsorProfile.query.get(sponsor_id)

        if not sponsor_profile:
            return make_response(jsonify({"error": "Sponsor profile not found"}), 404)

        campaigns_data = [
            {
                "id": campaign.id,
                "name": campaign.name,
                "status": campaign.status,
                "category": campaign.category,
                "budget": campaign.budget,
                "flagged": campaign.flagged,
                "start_date": campaign.start_date.strftime('%Y-%m-%d'),
                "end_date": campaign.end_date.strftime('%Y-%m-%d') if campaign.end_date else None,
                "type": campaign.type
            }
            for campaign in sponsor_profile.campaigns
        ]

        return make_response(jsonify({"campaigns": campaigns_data}), 200)

class CreateCampaign(Resource):
    @auth_token_required  
    def post(self):
        data = request.get_json()
        name = data.get('name')
        category = data.get('category')
        budget = data.get('budget')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        sponsor_profile_id = data.get('sponsor_profile_id')

        if not name or not category or not budget:
            return make_response(jsonify({"error": "Missing required fields"}), 400)

        if current_user.user_type != 'sponsor':
            return make_response(jsonify({"error": "User not authorized"}), 403)

        sponsor_profile = current_user.sponsor_profile
        if not sponsor_profile:
            return make_response(jsonify({"error": "Sponsor profile not found"}), 404)

        try:
            start_date = date.fromisoformat(start_date) if start_date else None
            end_date = date.fromisoformat(end_date) if end_date else None
        except ValueError:
            return make_response(jsonify({"error": "Invalid date format"}), 400)

        new_campaign = Campaign(
            name=name,
            category=category,
            budget=int(budget),
            sponsor_profile_id=sponsor_profile.id,
            start_date=start_date,
            end_date=end_date
        )
        
        db.session.add(new_campaign)
        db.session.commit()

        return make_response(jsonify({"message": "Campaign created successfully!"}), 201)

class EditCampaign(Resource):
    @auth_token_required  
    def put(self, campaign_id):
        campaign = Campaign.query.get(campaign_id)
        
        if not campaign:
            return make_response(jsonify({"error": "Campaign not found"}), 404)

        if current_user.user_type != 'sponsor' or campaign.sponsor_profile.user_id != current_user.id:
            return make_response(jsonify({"error": "User not authorized to edit this campaign"}), 403)

        data = request.get_json()
        name = data.get('name')
        status = data.get('status')
        category = data.get('category')
        budget = data.get('budget')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        campaign_type = data.get('type')  

        if name:
            campaign.name = name
        if status:
            campaign.status = status
        if category:
            campaign.category = category
        if budget:
            campaign.budget = int(budget)
        if start_date:
            try:
                campaign.start_date = date.fromisoformat(start_date)
            except ValueError:
                return make_response(jsonify({"error": "Invalid start date format"}), 400)
        if end_date:
            try:
                campaign.end_date = date.fromisoformat(end_date)
            except ValueError:
                return make_response(jsonify({"error": "Invalid end date format"}), 400)
        if campaign_type:
            if campaign_type not in ["public", "private"]:
                return make_response(jsonify({"error": "Invalid type value; must be 'public' or 'private'"}), 400)
            campaign.type = campaign_type  

        db.session.commit()

        return make_response(jsonify({"message": "Campaign updated successfully!"}), 200)

class DeleteCampaign(Resource):
    @auth_token_required
    def delete(self, campaign_id):
        campaign = Campaign.query.get(campaign_id)
        
        if not campaign:
            return make_response(jsonify({"error": "Campaign not found"}), 404)

        if current_user.user_type != 'sponsor' or campaign.sponsor_profile.user_id != current_user.id:
            return make_response(jsonify({"error": "User not authorized to delete this campaign"}), 403)

        for ad_request in campaign.ad_requests:
            db.session.delete(ad_request)
        
        db.session.delete(campaign)
        db.session.commit()

        return make_response(jsonify({"message": "Campaign and associated ad requests deleted successfully!"}), 200)

class CreateAdRequest(Resource):
    @auth_token_required
    def post(self, influencer_id):
        data = request.get_json()
        campaign_id = data.get('campaign_id')
        requirements = data.get('requirements')
        payment_amount = data.get('payment_amount')
        
        if not campaign_id or not requirements or not payment_amount:
            return make_response(jsonify({"error": "Missing required fields"}), 400)
        
        influencer = InfluencerProfile.query.get(influencer_id)
        if not influencer:
            return make_response(jsonify({"error": "Influencer not found"}), 404)

        campaign = Campaign.query.get(campaign_id)
        if not campaign or campaign.sponsor_profile.user_id != current_user.id:
            return make_response(jsonify({"error": "Campaign not found or not authorized"}), 403)

        new_ad_request = AdRequest(
            campaign_id=campaign_id,
            influencer_profile_id=influencer_id,
            requirements=requirements,
            payment_amount=float(payment_amount),
            status='Request Sent'
        )
        
        db.session.add(new_ad_request)
        db.session.commit()

        return make_response(jsonify({"message": "Ad request sent successfully!"}), 201)

class ViewAdRequests(Resource):
    @auth_token_required
    def get(self, campaign_id):
        campaign = Campaign.query.get(campaign_id)
        if not campaign or campaign.sponsor_profile.user_id != current_user.id:
            return make_response(jsonify({"error": "Campaign not found or not authorized"}), 403)

        ad_requests = AdRequest.query.filter_by(campaign_id=campaign_id).all()
        
        ad_requests_data = [
            {
                "id": req.id,
                "campaign_id": req.campaign_id,
                "influencer_profile_id": req.influencer_profile_id,
                "influencer_name": req.influencer_profile.name if req.influencer_profile else "N/A",
                "requirements": req.requirements,
                "flagged": req.flagged,
                "payment_amount": req.payment_amount,
                "status": req.status
            }
            for req in ad_requests
        ]

        return make_response(jsonify({"ad_requests": ad_requests_data}), 200)

class UpdateAdRequest(Resource):
    @auth_token_required
    def put(self, ad_request_id):
        ad_request = AdRequest.query.get(ad_request_id)
        
        if not ad_request:
            return make_response(jsonify({"error": "Ad request not found"}), 404)

        campaign = Campaign.query.get(ad_request.campaign_id)
        if campaign.sponsor_profile.user_id != current_user.id:
            return make_response(jsonify({"error": "User not authorized to update this ad request"}), 403)

        if ad_request.status != "Request Sent":
            return make_response(jsonify({"error": "Ad request cannot be edited in the current status"}), 400)

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

        db.session.commit()

        return make_response(jsonify({"message": "Ad request updated successfully!"}), 200)

class DeleteAdRequest(Resource):
    @auth_token_required
    def delete(self, ad_request_id):
        ad_request = AdRequest.query.get(ad_request_id)
        
        if not ad_request:
            return make_response(jsonify({"error": "Ad request not found"}), 404)

        campaign = Campaign.query.get(ad_request.campaign_id)
        if campaign.sponsor_profile.user_id != current_user.id:
            return make_response(jsonify({"error": "User not authorized to delete this ad request"}), 403)

        if ad_request.status != "Request Sent" and ad_request.status != "Request Negotiated":
            return make_response(jsonify({"error": "Ad request cannot be deleted as it has already been accepted or rejected"}), 400)

        db.session.delete(ad_request)
        db.session.commit()

        return make_response(jsonify({"message": "Ad request deleted successfully!"}), 200)
