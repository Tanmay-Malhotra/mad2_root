from flask_restful import Resource
from flask import jsonify, make_response, request
from flask_security import login_user, verify_password
from backend.models import db, user_datastore, InfluencerProfile, SponsorProfile


# API for login and signup 

class Signin(Resource):
    def post(self):
        data = request.get_json()
        email = data['email']
        password = data['password']
        
        if not email:
            return make_response(jsonify({"message": "email is required"}), 400)
        if not password:
            return make_response(jsonify({"message": "password is required"}), 400)
        
        # Find the user by email
        user = user_datastore.find_user(email=email)
        if user:
            if verify_password(password, user.password):
                token = user.get_auth_token()
                if token:
                    login_user(user)
                    db.session.commit()
                return make_response(jsonify({
                    "message": "login successful",
                    "authToken": token,
                    "email": user.email,
                    "role": user.roles[0].name,  # assuming the user has only one role
                    "id": user.id
                }), 200)
            else:
                return make_response(jsonify({"message": "invalid password"}), 401)
        
        return make_response(jsonify({"message": "user not found"}), 404)
    
class InfluencerSignup(Resource):
    def post(self):
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        industry = data.get('industry')
        platform = data.get('platform')
        followers = data.get('followers')

        # Basic validation for required fields
        if not name:
            return make_response(jsonify({"message": "name is required"}), 400)
        if not email:
            return make_response(jsonify({"message": "email is required"}), 400)
        if not password:
            return make_response(jsonify({"message": "password is required"}), 400)
        if not industry:
            return make_response(jsonify({"message": "industry is required"}), 400)
        if not platform:
            return make_response(jsonify({"message": "platform is required"}), 400)
        if not followers or not isinstance(followers, int):
            return make_response(jsonify({"message": "followers count is required and should be an integer"}), 400)

        # Check if user already exists
        if user_datastore.find_user(email=email):
            return make_response(jsonify({"message": "user already exists", "email": email}), 409)

        # Create new influencer user with only User model fields
        user = user_datastore.create_user(
            email=email,
            password=password,
            user_type='influencer'
        )
        user_datastore.add_role_to_user(user, "influencer")
        db.session.commit()

        # Create InfluencerProfile linked to the user
        influencer_profile = InfluencerProfile(
            user_id=user.id,
            name=name,
            industry=industry,
            platform=platform,
            followers=followers
        )
        db.session.add(influencer_profile)
        db.session.commit()

        return make_response(jsonify({
            "message": "influencer created",
            "id": user.id,
            "email": user.email
        }), 201)

class SponsorSignup(Resource):
    def post(self):
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        industry = data.get('industry')

        # Basic validation for required fields
        if not name:
            return make_response(jsonify({"message": "name is required"}), 400)
        if not email:
            return make_response(jsonify({"message": "email is required"}), 400)
        if not password:
            return make_response(jsonify({"message": "password is required"}), 400)
        if not industry:
            return make_response(jsonify({"message": "industry is required"}), 400)

        # Check if sponsor already exists
        if user_datastore.find_user(email=email):
            return make_response(jsonify({"message": "user already exists", "email": email}), 409)

        # Create new sponsor user with only User model fields
        user = user_datastore.create_user(
            email=email,
            password=password,
            user_type='sponsor'
        )
        user_datastore.add_role_to_user(user, "sponsor")
        db.session.commit()

        # Create SponsorProfile linked to the user
        sponsor_profile = SponsorProfile(
            user_id=user.id,
            name=name,
            industry=industry
        )
        db.session.add(sponsor_profile)
        db.session.commit()

        return make_response(jsonify({
            "message": "sponsor created, awaiting admin approval",
            "id": user.id,
            "email": user.email
        }), 201)


