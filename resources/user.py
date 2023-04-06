from flask_restful import Resource, reqparse
from flask import request, session, jsonify, make_response
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from bson.objectid import ObjectId
from models.user import User
from models.nailtech import NailTech
from models.customer import Customer
from datetime import datetime

class SingleUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=False, help='name is required')
    parser.add_argument('email', type=str, required=False, help='Email is required.')
    parser.add_argument('password', type=str, required=False, help='Password is required.')
    parser.add_argument('is_customer', type=bool, default=False)
    parser.add_argument('is_nail_tech', type=bool, default=False)

    def post(self):
        data = SingleUser.parser.parse_args()
        name = data['name']
        email = data['email']
        password = data['password']
        is_customer = data['is_customer']
        is_nail_tech = data['is_nail_tech']

        nailtech = NailTech.objects(email=email).first()
        customer = Customer.objects(email=email).first()
        if nailtech:
            return make_response(jsonify(nailtech=nailtech))
        elif customer:
            return make_response(jsonify(customer=customer))
        if is_nail_tech:
            nailtech = NailTech(name=name, email=email, password=password)
            nailtech.save()
            access_token = create_access_token(identity=str(nailtech.id))
            return {'message': 'User created successfully.', 'nailtech_id': str(nailtech.id), 'access_token': access_token}, 201
        elif is_customer:
            customer = Customer(name=name, email=email, password=password)
            customer.save()
            access_token = create_access_token(identity=str(customer.id))
            return {'message': 'User created successfully.', 'customer_id': str(customer.id), 'access_token': access_token}, 201
        else:
            user = User(name=name, email=email, password=password, is_customer=is_customer, is_nail_tech=is_nail_tech)
            user.save()
            access_token = create_access_token(identity=str(user.id))
            return {'message': 'User created successfully.', 'user_id': str(user.id), 'access_token': access_token}, 201
       

    @jwt_required()
    def put(self, user_id):
        user = User.objects(id=ObjectId(user_id)).first()
        if not user:
            return {'message': 'User not found.'}, 404

        data = SingleUser.parser.parse_args()
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.password = data.get('password', user.password)
        user.is_customer = data.get('is_customer', user.is_customer)
        user.is_nail_tech = data.get('is_nail_tech', user.is_nail_tech)
        user.modified_date = datetime.now()
        user.save()
        return {'message': 'User updated successfully.'}, 200

    @jwt_required()
    def delete(self, user_id):
        user = User.objects(id=ObjectId(user_id)).first()
        if not user:
            return {'message': 'User not found.'}, 404

        user.delete()
        return {'message': 'User deleted successfully.'}, 200

class LoginUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, help='Email is required.')
    parser.add_argument('password', type=str, required=True, help='Password is required.')

    def post(self):
        data = SingleUser.parser.parse_args()
        email = data['email']
        password = data['password']
        existing_user = User.objects(email=email, password=password).first()
        nailtech = NailTech.objects(email=email, password=password).first()
        customer = Customer.objects(email=email, password=password).first()
        if existing_user:
            return make_response(jsonify(user=existing_user))
        elif nailtech:
            return make_response(jsonify(nailtech=nailtech))
        elif customer:
            return make_response(jsonify(customer=customer))



     
