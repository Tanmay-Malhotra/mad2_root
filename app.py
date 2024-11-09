from flask import Flask
from backend.config import LocalDevelopmentConfig
from backend.models import db, User, Role, datastore
from flask_security import Security, SQLAlchemyUserDatastore, auth_required
from backend.routes.auth import Signin, InfluencerSignup, SponsorSignup
from flask_restful import Api

def createApp():
    app = Flask(__name__)
    api_handler = Api(app)

    app.config.from_object(LocalDevelopmentConfig)


    # model init
    db.init_app(app)



    #flask security
    #security = Security(app, user_datastore)

    user_datastore = datastore
    app.security = Security(app, datastore=user_datastore)
    app.app_context().push() 

    return app, api_handler

app, api_handler = createApp()

#import backend.initial_data

@app.get('/')
def home():
    return '<h1> home page</h1>'

@app.get('/protected')
@auth_required()
def protected():
    return '<h1> only accessible by auth user</h1>'

#----------------API Routes-----------------------------------------------------

from backend.routes.auth import Signin, InfluencerSignup, SponsorSignup
api_handler.add_resource(Signin, "/signin")
api_handler.add_resource(InfluencerSignup, "/signup")
api_handler.add_resource(SponsorSignup, "/sponsor/signup")


if (__name__ == '__main__'):
    app.run()