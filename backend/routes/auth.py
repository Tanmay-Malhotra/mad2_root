""" from flask_restful import Resource
from flask import jsonify, make_response, request
from flask_security import login_user, verify_password
from backend.models import db, user_datastore

#API for login and signup 


class Signin(Resource):
    #User datastore is not accessed ????
    def __init__(self, user_datastore):
        self.user_datastore = user_datastore 
    def post(self):
        data = request.get_json()
        email = data['email']
        password = data['password']
        if not email:
            return make_response(jsonify({"message": "email is required"}), 400)
        if not password:
            return make_response(jsonify({"message": "password is required"}), 400)
        
        user = datastore.find_user(email=email)
        if user:
            if verify_password(password, user.password):
                token = user.get_auth_token()
                if token:
                    login_user(user)
                    db.session.commit()
                return make_response(jsonify({"message": "login successful", "authToken": token, "email": user.email, "role": user.roles[0].name, "id": user.id}), 200)
            else:
                return make_response(jsonify({"message": "invalid password"}), 401)        
        return make_response(jsonify({"message": "user not found", "email": user.email}), 404)
    
    from flask import request, jsonify, make_response
from flask_restful import Resource

# Influencer Signup Class with additional fields
class InfluencerSignup(Resource):
    def __init__(self, user_datastore):
        self.user_datastore = user_datastore 

    def post(self):
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')
        industry = data.get('industry')  # New field for industry
        platform = data.get('platform')  # Platform
        followers = data.get('followers')  # Expected to be an integer

        # Basic validation for required fields
        if not name:
            return make_response(jsonify({"message": "name is required"}), 400)
        if not email:
            return make_response(jsonify({"message": "email is required"}), 400)
        if not password:
            return make_response(jsonify({"message": "password is required"}), 400)
        if not username:
            return make_response(jsonify({"message": "username is required"}), 400)
        if not industry:
            return make_response(jsonify({"message": "industry is required"}), 400)
        if not platform :
            return make_response(jsonify({"message": "platform_presence is required"}), 400)
        if not followers or not isinstance(followers, int):
            return make_response(jsonify({"message": "followers count is required and should be an integer"}), 400)

        # Check if user already exists
        if user_datastore.find_user(email=email):
            return make_response(jsonify({"message": "user already exists", "email": email}), 409)

        # Create new influencer user
        user = user_datastore.create_user(
            name=name,
            email=email,
            password=password,
            username=username,
            industry=industry,
            platform=platform,
            followers=followers
        )

        # Add the 'influencer' role to the user
        user_datastore.add_role_to_user(user, "influencer")
        db.session.commit()
        return make_response(jsonify({"message": "influencer created", "id": user.id, "email": user.email}), 201)
    
class SponsorSignup(Resource):
    def post(self):
        data = request.get_json()
        name = data.get('name')
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        industry = data.get('industry')

        # Basic validation for required fields
        if not name:
            return make_response(jsonify({"message": "name is required"}), 400)
        if not username:
            return make_response(jsonify({"message": "username is required"}), 400)
        if not password:
            return make_response(jsonify({"message": "password is required"}), 400)
        if not email:
            return make_response(jsonify({"message": "email is required"}), 400)
        if not industry:
            return make_response(jsonify({"message": "industry is required"}), 400)

        # Check if sponsor already exists
        if user_datastore.find_user(email=email):
            return make_response(jsonify({"message": "user already exists", "email": email}), 409)

        # Create new sponsor with 'Pending' approval status
        user = user_datastore.create_user(
            name=name,
            username=username,
            password=password,
            email=email,
            industry=industry,
            approval_status="Pending"
        )

        # Add the 'sponsor' role to the user
        user_datastore.add_role_to_user(user, "sponsor")
        db.session.commit()
        return make_response(jsonify({"message": "sponsor created, awaiting admin approval", "id": user.id, "email": user.email}), 201)

 """
        
from flask_restful import Resource
from flask import jsonify, make_response, request
from flask_security import login_user, verify_password
from backend.models import db, user_datastore

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
        username = data.get('username')
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
        if not username:
            return make_response(jsonify({"message": "username is required"}), 400)
        if not industry:
            return make_response(jsonify({"message": "industry is required"}), 400)
        if not platform:
            return make_response(jsonify({"message": "platform_presence is required"}), 400)
        if not followers or not isinstance(followers, int):
            return make_response(jsonify({"message": "followers count is required and should be an integer"}), 400)

        # Check if user already exists
        if user_datastore.find_user(email=email):
            return make_response(jsonify({"message": "user already exists", "email": email}), 409)

        # Create new influencer user with profile-specific fields
        user = user_datastore.create_user(
            name=name,
            email=email,
            password=password,
            username=username,
            industry=industry,
            platform=platform,
            followers=followers,
            user_type='influencer'
        )

        # Add the 'influencer' role to the user
        user_datastore.add_role_to_user(user, "influencer")
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
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        industry = data.get('industry')

        # Basic validation for required fields
        if not name:
            return make_response(jsonify({"message": "name is required"}), 400)
        if not username:
            return make_response(jsonify({"message": "username is required"}), 400)
        if not password:
            return make_response(jsonify({"message": "password is required"}), 400)
        if not email:
            return make_response(jsonify({"message": "email is required"}), 400)
        if not industry:
            return make_response(jsonify({"message": "industry is required"}), 400)

        # Check if sponsor already exists
        if user_datastore.find_user(email=email):
            return make_response(jsonify({"message": "user already exists", "email": email}), 409)

        # Create new sponsor with profile-specific fields
        user = user_datastore.create_user(
            name=name,
            username=username,
            password=password,
            email=email,
            industry=industry,
            approval_status="Pending",
            user_type='sponsor'
        )

        # Add the 'sponsor' role to the user
        user_datastore.add_role_to_user(user, "sponsor")
        db.session.commit()
        
        return make_response(jsonify({
            "message": "sponsor created, awaiting admin approval",
            "id": user.id,
            "email": user.email
        }), 201)
