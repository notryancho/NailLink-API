from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask import Flask
from flask_mongoengine import MongoEngine
from resources.appointment import SingleAppointment, AllAppointments
from resources.customer import SingleCustomer, AllCustomers
from resources.nailtech import SingleNailTech, AllNailTechs
from resources.review import Review
from resources.service import Services, AllServices
from resources.user import SingleUser, LoginUser
from flask_session import Session
from dotenv import load_dotenv
from flask_restful import Api
from flask_cors import CORS
from models.db import db
import datetime
import secrets
import os

load_dotenv()

APP_SECRET_KEY = secrets.token_hex(32)
MONGO_URI = os.getenv('MONGO_URI')
app = Flask(__name__)
CORS(app)

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
app.config["MONGODB_SETTINGS"] = {'DB': "TEST", "host": MONGO_URI}
app.config['JWT_SECRET_KEY'] = APP_SECRET_KEY
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False


Session(app)
jwt = JWTManager(app)
api = Api(app)
db.init_app(app, print('started'))

api.add_resource(SingleUser, '/user')
api.add_resource(LoginUser, '/login')
api.add_resource(SingleAppointment, '/appointment/<id>')
api.add_resource(SingleCustomer, '/customer/<id>')
api.add_resource(SingleNailTech, '/nailtech/<id>')
api.add_resource(Review, '/review')
api.add_resource(Services, '/service')
api.add_resource(AllServices, '/all-services')
api.add_resource(AllNailTechs, '/all-nailtechs')
api.add_resource(AllCustomers, '/all-customers')
api.add_resource(AllAppointments, '/all-appointments')

if __name__ == "__main__":
    app.run(debug=True)


   


