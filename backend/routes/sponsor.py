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
