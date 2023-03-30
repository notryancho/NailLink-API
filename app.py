# import os
# from models.db import db
# from flask import Flask, request, session, jsonify
# from flask_mongoengine import MongoEngine 
# from mongoengine import connect, Document, ReferenceField, ListField, StringField, EmailField, IntField, FloatField, DateField, BooleanField
# from mongoengine.fields import DateTimeField
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
# from bson.objectid import ObjectId
# from dotenv import load_dotenv
# from flask_cors import CORS
# from flask_restful import Api
# from models.user import UserModel
# import datetime 
# from resources.user import User 
# from resources.appointment import Appointment
# from resources.customer import Customer
# from resources.nailtech import NailTech
# from resources.service import Service
# from resources.review import Review


# load_dotenv() 


# SECRET_KEY = os.environ.get('SECRET_KEY')
# APP_ENV = os.environ.get('APP_ENV')
# DEBUG = os.environ.get('DEBUG')
# MONGO_URI = os.environ.get('MONGO_URI')
# SALT_ROUNDS = os.environ.get('SALT_ROUNDS')

# app = Flask(__name__)
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# app.config['JWT_SECRET_KEY'] = SECRET_KEY
# app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
# app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY')

# CORS(app)
# JWTManager(app)
# bcrypt = Bcrypt(app)
# db = MongoEngine(app)
# api = Api(app)

# # from resources.user import User 
# # from resources.appointment import Appointment
# # from resources.customer import Customer
# # from resources.nailtech import NailTech
# # from resources.service import Service
# # from resources.review import Review

# api.add_resource(Appointment, '/appointment')
# api.add_resource(Customer, '/customer')
# api.add_resource(NailTech, '/nailtech')
# api.add_resource(Review, '/review')
# api.add_resource(Service, '/service')
# api.add_resource(User, '/user') 

# @app.route('/login', methods=['POST'])
# def login():
#     email = request.json.get('email', None)
#     password = request.json.get('password', None)
#     user = User.objects(email=email).first()
#     if not user or not user.password == password:
#         return jsonify({"msg": "Invalid email or password"}), 401
#     access_token = create_access_token(identity=str(user.id))
#     return jsonify(access_token=access_token)

# @app.route("/register", methods=['POST'])
# def register_customer():
#     user = User()
#     customer = Customer()
#     body = request.get_json()
#     email = User.objects(email=body.get("email")).first()
#     if email:
#         return {"message": "Email already exists"}, 500
#     hashed = bcrypt.generate_password_hash(body.get("password"), int(SALT_ROUNDS))
#     user.email = body.get("email")
#     user.password = hashed
#     user.is_customer = True
#     user.is_nail_tech = False
#     user.save()
#     customer.user_id = user.id
#     customer.name = body.get("name")
#     customer.save()
#     return {"message": "User created"}, 200

# @app.route('/protected', methods=['GET'])
# @jwt_required()
# def protected():
#     user_id = get_jwt_identity()
#     user = User.objects(id=user_id).first()
#     return jsonify({"email": user.email, "is_customer": user.is_customer, "is_nail_tech": user.is_nail_tech})

# if __name__ == '__main__':
#     app.run(debug=True)

from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask import Flask
from flask_mongoengine import MongoEngine
from resources.appointment import Appointment
from resources.customer import Customer
from resources.nailtech import NailTech
from resources.review import Review
from resources.service import Service
from resources.user import User
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

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
app.config["MONGODB_SETTINGS"] = {'DB': "TEST", "host": MONGO_URI}
app.config['JWT_SECRET_KEY'] = APP_SECRET_KEY
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False

CORS(app)
Session(app)
jwt = JWTManager(app)
api = Api(app)
db.init_app(app, print('started'))

api.add_resource(User, '/user')
api.add_resource(Appointment, '/appointment')
api.add_resource(Customer, '/customer')
api.add_resource(NailTech, '/nailtech')
api.add_resource(Review, '/review')
api.add_resource(Service, '/service')



if __name__ == "__main__":
    app.run(debug=True)

   


