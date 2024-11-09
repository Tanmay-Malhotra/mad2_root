from flask import request
from flask import Flask

""" from backend.config import LocalDevelopmentConfig
from backend.models import db, User, Role, datastore
from flask_security import Security, SQLAlchemyUserDatastore, auth_required
from backend.routes.auth import Signin, InfluencerSignup, SponsorSignup
from flask_restful import Api """




def createApp():
    app = Flask(__name__)
    from backend.config import LocalDevelopmentConfig
    app.config.from_object(LocalDevelopmentConfig)

    from backend.models import db, user_datastore

    db.init_app(app)

    from flask_security import Security
    security = Security(app, user_datastore)

    from flask_restful import Api
    api = Api(app)

    from flask_cors import CORS
    CORS(app)

    return app, api

app, api_handler = createApp()
from flask_security import auth_required
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