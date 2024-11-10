#campaign and ad request management api for sponsor
from flask import request, session, jsonify, make_response
from flask_restful import Resource
from flask_security import auth_token_required, current_user
from datetime import date

from backend.models import db, Campaign,SponsorProfile,User

class Campaigns(Resource):
    @auth_token_required  # Require a valid authentication token
    def get(self):
        # Get sponsor_id from query parameters
        sponsor_id = request.args.get('sponsor_id')
        
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




