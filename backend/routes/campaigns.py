#campaign and ad request management api for sponsor
from flask import request, session, jsonify, make_response
from flask_restful import Resource
from flask_security import auth_token_required, current_user
from datetime import date

from backend.models import db, Campaign,SponsorProfile,User
from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_security import auth_token_required, current_user
from datetime import date

from backend.models import db, Campaign

class Campaigns(Resource):
    @auth_token_required  # Require a valid authentication token
    def get(self, sponsor_id):
        # Ensure sponsor_id is provided
        if not sponsor_id:
            return make_response(jsonify({"error": "Sponsor ID is required"}), 400)

        # Retrieve the sponsor profile by sponsor_id
        sponsor_profile = SponsorProfile.query.get(sponsor_id)
        
        # Ensure sponsor_profile exists
        if not sponsor_profile:
            return make_response(jsonify({"error": "Sponsor profile not found"}), 404)

        # Retrieve and format the campaigns associated with this sponsor
        campaigns_data = [
            {
                "id": campaign.id,
                "name": campaign.name,
                "status": campaign.status,
                "category": campaign.category,
                "budget": campaign.budget,
                "flagged": campaign.flagged,
                "start_date": campaign.start_date.strftime('%Y-%m-%d'),
                "end_date": campaign.end_date.strftime('%Y-%m-%d') if campaign.end_date else None
            }
            for campaign in sponsor_profile.campaigns
        ]

        return make_response(jsonify({"campaigns": campaigns_data}), 200)



class CreateCampaign(Resource):
    @auth_token_required  # Require a valid token to access
    def post(self):
        # Parse data from JSON request
        data = request.get_json()
        name = data.get('name')
        category = data.get('category')
        budget = data.get('budget')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        sponsor_profile_id = data.get('sponsor_profile_id')

        # Validate required fields
        if not name or not category or not budget:
            return make_response(jsonify({"error": "Missing required fields"}), 400)

        # Check if the current user is a sponsor
        # Make some changes here for influencer to view public campaigns ?
        if current_user.user_type != 'sponsor':
            return make_response(jsonify({"error": "User not authorized"}), 403)

        # Get sponsor profile from current_user
        sponsor_profile = current_user.sponsor_profile
        if not sponsor_profile:
            return make_response(jsonify({"error": "Sponsor profile not found"}), 404)

        # Convert start_date and end_date to date objects if provided
        try:
            start_date = date.fromisoformat(start_date) if start_date else None
            end_date = date.fromisoformat(end_date) if end_date else None
        except ValueError:
            return make_response(jsonify({"error": "Invalid date format"}), 400)

        # Create a new campaign

        #Add check for duplicate campaign, a similar campaign already exists ?
        new_campaign = Campaign(
            name=name,
            category=category,
            budget=int(budget),
            sponsor_profile_id=sponsor_profile.id,
            start_date=start_date,
            end_date=end_date
        )
        
        # Add to database and commit
        db.session.add(new_campaign)
        db.session.commit()

        return make_response(jsonify({"message": "Campaign created successfully!"}), 201)



# edit campaign 
# Use put for edit campaign, only works for campaigns that already exist
class EditCampaign(Resource):
    @auth_token_required  # Require a valid authentication token
    def put(self, campaign_id):
        print("Reached EditCampaign PUT method")
        # Find the campaign by campaign_id
        campaign = Campaign.query.get(campaign_id)
        
        # Ensure the campaign exists
        if not campaign:
            return make_response(jsonify({"error": "Campaign not found"}), 404)

        # Verify that the current user is authorized to edit this campaign
        if current_user.user_type != 'sponsor' or campaign.sponsor_profile.user_id != current_user.id:
            return make_response(jsonify({"error": "User not authorized to edit this campaign"}), 403)

        # Parse data from JSON request
        data = request.get_json()
        name = data.get('name')
        status = data.get('status')
        category = data.get('category')
        budget = data.get('budget')
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        # Update campaign details with new values if they are provided
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

        # Commit the changes to the database
        db.session.commit()

        return make_response(jsonify({"message": "Campaign updated successfully!"}), 200)
    

        
from flask import jsonify, make_response
from flask_restful import Resource
from flask_security import auth_token_required, current_user
from backend.models import db, Campaign

class DeleteCampaign(Resource):
    @auth_token_required  # Require a valid authentication token
    def delete(self, campaign_id):
        print("Reached DeleteCampaign DELETE method")  # Debug statement

        # Find the campaign by campaign_id
        campaign = Campaign.query.get(campaign_id)
        
        # Ensure the campaign exists
        if not campaign:
            return make_response(jsonify({"error": "Campaign not found"}), 404)

        # Verify that the current user is authorized to delete this campaign
        if current_user.user_type != 'sponsor' or campaign.sponsor_profile.user_id != current_user.id:
            return make_response(jsonify({"error": "User not authorized to delete this campaign"}), 403)

        # Delete the campaign
        db.session.delete(campaign)
        db.session.commit()

        return make_response(jsonify({"message": "Campaign deleted successfully!"}), 200)


#-------------------------------------AD Request for sponsors----------------------------------------------------------

from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_security import auth_token_required
from backend.models import db, AdRequest, Campaign, InfluencerProfile

class CreateAdRequest(Resource):
    @auth_token_required
    def post(self, influencer_id):
        data = request.get_json()
        campaign_id = data.get('campaign_id')
        requirements = data.get('requirements')
        payment_amount = data.get('payment_amount')
        
        # Check if all required fields are provided
        if not campaign_id or not requirements or not payment_amount:
            return make_response(jsonify({"error": "Missing required fields"}), 400)
        
        # Verify if the influencer exists
        influencer = InfluencerProfile.query.get(influencer_id)
        if not influencer:
            return make_response(jsonify({"error": "Influencer not found"}), 404)

        # Verify if the campaign exists and belongs to the sponsor
        campaign = Campaign.query.get(campaign_id)
        if not campaign or campaign.sponsor_profile.user_id != current_user.id:
            return make_response(jsonify({"error": "Campaign not found or not authorized"}), 403)

        # Create the ad request
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
    
# DO I NEED THE METHOD BELOW ?
""" class ViewAdRequests(Resource):
    @auth_token_required
    def get(self, campaign_id):
        # Verify if the campaign exists and if the current user is authorized
        campaign = Campaign.query.get(campaign_id)
        if not campaign or campaign.sponsor_profile.user_id != current_user.id:
            return make_response(jsonify({"error": "Campaign not found or not authorized"}), 403)

        # Fetch all ad requests for the specified campaign
        ad_requests = AdRequest.query.filter_by(campaign_id=campaign_id).all()
        
        # Manually convert each ad request to dictionary format
        ad_requests_data = [
            {
                "id": req.id,
                "campaign_id": req.campaign_id,
                "influencer_profile_id": req.influencer_profile_id,
                "requirements": req.requirements,
                "flagged": req.flagged,
                "payment_amount": req.payment_amount,
                "status": req.status
            }
            for req in ad_requests
        ]

        return make_response(jsonify({"ad_requests": ad_requests_data}), 200) """
    
class ViewAdRequests(Resource):
    @auth_token_required
    def get(self, campaign_id):
        # Verify if the campaign exists and if the current user is authorized
        campaign = Campaign.query.get(campaign_id)
        if not campaign or campaign.sponsor_profile.user_id != current_user.id:
            return make_response(jsonify({"error": "Campaign not found or not authorized"}), 403)

        # Fetch all ad requests for the specified campaign
        ad_requests = AdRequest.query.filter_by(campaign_id=campaign_id).all()
        
        # Manually convert each ad request to dictionary format with influencer name
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

# Update Ad Request 
class UpdateAdRequest(Resource):
    @auth_token_required
    def put(self, ad_request_id):
        # Get the ad request by ad_request_id
        ad_request = AdRequest.query.get(ad_request_id)
        
        # Verify if the ad request exists
        if not ad_request:
            return make_response(jsonify({"error": "Ad request not found"}), 404)

        # Verify if the current user is authorized to update this ad request
        campaign = Campaign.query.get(ad_request.campaign_id)
        if campaign.sponsor_profile.user_id != current_user.id:
            return make_response(jsonify({"error": "User not authorized to update this ad request"}), 403)

        # Parse data from the JSON request
        data = request.get_json()
        requirements = data.get('requirements')
        payment_amount = data.get('payment_amount')
        status = data.get('status')

        # Update ad request details with new values if they are provided
        if requirements is not None:
            ad_request.requirements = requirements
        if payment_amount is not None:
            try:
                ad_request.payment_amount = float(payment_amount)
            except ValueError:
                return make_response(jsonify({"error": "Invalid payment amount"}), 400)
        if status is not None:
            ad_request.status = status

        # Commit the changes to the database
        db.session.commit()

        return make_response(jsonify({"message": "Ad request updated successfully!"}), 200)



class DeleteAdRequest(Resource):
    @auth_token_required
    def delete(self, ad_request_id):
        # Get the ad request by ad_request_id
        ad_request = AdRequest.query.get(ad_request_id)
        
        # Verify if the ad request exists
        if not ad_request:
            return make_response(jsonify({"error": "Ad request not found"}), 404)

        # Verify if the current user is authorized to delete this ad request
        campaign = Campaign.query.get(ad_request.campaign_id)
        if campaign.sponsor_profile.user_id != current_user.id:
            return make_response(jsonify({"error": "User not authorized to delete this ad request"}), 403)

        # Check if the ad request status is "Request Sent"
        if ad_request.status != "Request Sent":
            return make_response(jsonify({"error": "Ad request cannot be deleted as it has already been accepted or rejected"}), 400)

        # Delete the ad request
        db.session.delete(ad_request)
        db.session.commit()

        return make_response(jsonify({"message": "Ad request deleted successfully!"}), 200)




