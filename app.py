from flask import Flask, jsonify
from flask_security import Security, SQLAlchemyUserDatastore, auth_required
from flask_restful import Api
from flask_cors import CORS
from backend.models import db, User, Role  # Ensure these imports are correct
from backend.routes.auth import Signin, InfluencerSignup, SponsorSignup

def createApp():
    app = Flask(__name__)
    
    # Load configuration
    from backend.config import LocalDevelopmentConfig
    app.config.from_object(LocalDevelopmentConfig)
    
    # Initialize database
    db.init_app(app)
    
    # Set up Flask-Security with SQLAlchemyUserDatastore
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    # Initialize API and CORS
    api = Api(app)
    CORS(app)

    return app, api

# Create the app and API handler
app, api_handler = createApp()

# Example of a protected route using Flask-Security
@app.get('/protected')
@auth_required()  # Requires authenticated user
def protected():
    return '<h1>Only accessible by authenticated user</h1>'

#----------------API Routes-----------------------------------------------------

# Add resources for API routes
api_handler.add_resource(Signin, "/signin")
api_handler.add_resource(InfluencerSignup, "/signup/influencer")  # Separate endpoint for influencers
api_handler.add_resource(SponsorSignup, "/signup/sponsor")       # Separate endpoint for sponsors

if __name__ == '__main__':
    app.run()
