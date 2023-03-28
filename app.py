import os
from flask import Flask, jsonify, request, abort
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from dotenv import load_dotenv


load_dotenv() 


SECRET_KEY = os.environ.get('SECRET_KEY')
APP_ENV = os.environ.get('APP_ENV')
DEBUG = os.environ.get('DEBUG')
MONGO_URI = os.environ.get('MONGO_URI')

app = Flask(__name__)
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY')
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# routes for registering and signing in users
@app.route('/register', methods=['POST'])
def register():
    # check if user already exists in database
    existing_user = mongo.db.users.find_one({'email': request.json['email']})
    if existing_user:
        abort(400, 'User with that email already exists')

    # hash password and create new user
    hashed_password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
    is_customer = request.json.get('is_customer', False)
    is_nail_tech = request.json.get('is_nail_tech', False)
    if not is_customer and not is_nail_tech:
        abort(400, 'User must be either a customer or a nail tech')
    user = {'name': request.json['name'], 'email': request.json['email'], 'password': hashed_password, 'is_customer': is_customer, 'is_nail_tech': is_nail_tech}
    result = mongo.db.users.insert_one(user)

    # create access token and return response
    access_token = create_access_token(identity=str(result.inserted_id))
    return jsonify({'access_token': access_token}), 201

@app.route('/signin', methods=['POST'])
def signin():
    # check if user exists in database
    user = mongo.db.users.find_one({'email': request.json['email']})
    if not user:
        abort(401, 'Invalid email or password')

    # check if password is correct
    if not bcrypt.check_password_hash(user['password'], request.json['password']):
        abort(401, 'Invalid email or password')

    # create access token and return response
    access_token = create_access_token(identity=str(user['_id']))
    return jsonify({'access_token': access_token}), 200

# routes for customers
@app.route('/customers/<id>', methods=['GET'])
@jwt_required()
def get_customer(id):
    # check if user is a customer
    current_user_id = get_jwt_identity()
    current_user = mongo.db.users.find_one({'_id': ObjectId(current_user_id)})
    if not current_user['is_customer']:
        abort(403, 'Forbidden')

    customer = mongo.db.customers.find_one({'_id': ObjectId(id)})
    if not customer:
        abort(404, 'Customer not found')
    output = {'id': str(customer['_id']), 'name': customer['name'], 'email': customer['email']}
    return jsonify({'result': output})

@app.route('/customers', methods=['POST'])
@jwt_required()
def add_customer():
# check if user is a nail tech
    current_user_id = get_jwt_identity()
    current_user = mongo.db.users.find_one({'_id': ObjectId(current_user_id)})
    if not current_user['is_nail_tech']:
        abort(403, 'Forbidden')
        #create a new customer
    customer = {'name': request.json['name'], 'email': request.json['email']}
    result = mongo.db.customers.insert_one(customer)
    return jsonify({'message': 'Customer added successfully', 'id': str(result.inserted_id)}), 201

@app.route('/customers/<id>', methods=['PUT'])
@jwt_required()
def update_customer(id):
# check if user is a nail tech
    current_user_id = get_jwt_identity()
    current_user = mongo.db.users.find_one({'_id': ObjectId(current_user_id)})
    if not current_user['is_nail_tech']:
        abort(403, 'Forbidden') 
    # check if customer exists
    customer = mongo.db.customers.find_one({'_id': ObjectId(id)})
    if not customer:
        abort(404, 'Customer not found')
# update customer
    mongo.db.customers.update_one({'_id': ObjectId(id)}, {'$set': request.json})
# return response
    return jsonify({'message': 'Customer updated successfully'})

@app.route('/customers/<id>', methods=['DELETE'])
@jwt_required()
def delete_customer(id):
# check if user is a nail tech
    current_user_id = get_jwt_identity()
    current_user = mongo.db.users.find_one({'_id': ObjectId(current_user_id)})
    if not current_user['is_nail_tech']:
        abort(403, 'Forbidden')
# check if customer exists
    customer = mongo.db.customers.find_one({'_id': ObjectId(id)})
    if not customer:
        abort(404, 'Customer not found')
    # delete customer
    mongo.db.customers.delete_one({'_id': ObjectId(id)})
    # return response
    return jsonify({'message': 'Customer deleted successfully'})

@app.route('/nailtechs', methods=['GET'])
@jwt_required()
def get_nail_techs():
# check if user is a customer
    current_user_id = get_jwt_identity()
    current_user = mongo.db.users.find_one({'_id': ObjectId(current_user_id)})
    if not current_user['is_customer']:
        abort(403, 'Forbidden')
    nail_techs = mongo.db.users.find({'is_nail_tech': True})
    output = []
    for nail_tech in nail_techs:
        output.append({'id': str(nail_tech['_id']), 'name': nail_tech['name'], 'email': nail_tech['email']})
    return jsonify({'result': output})

@app.route('/nailtechs/<id>', methods=['GET'])
@jwt_required()
def get_nail_tech(id):
# check if user is a customer
    current_user_id = get_jwt_identity()
    current_user = mongo.db.users.find_one({'_id': ObjectId(current_user_id)})
    if not current_user['is_customer']:
        abort(403, 'Forbidden')
    nail_tech = mongo.db.users.find_one({'_id': ObjectId(id), 'is_nail_tech': True})
    if not nail_tech:
        abort(404, 'Nail tech not found')
    output = {'id': str(nail_tech['_id']), 'name': nail_tech['name'], 'email': nail_tech['email']}

   


