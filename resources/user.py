from flask_restful import Resource, reqparse
from flask import request, session, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from models.user import User


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, help='Email is required.')
    parser.add_argument('password', type=str, required=True, help='Password is required.')

    @jwt_required()
    def get(self, user_id):
        user = User.objects(id=ObjectId(user_id)).first()
        if not user:
            return {'message': 'User not found.'}, 404
        return {'email': user.email, 'is_customer': user.is_customer, 'is_nail_tech': user.is_nail_tech}, 200

    def post(self):
        data = User.parser.parse_args()
        email = data['email']
        password = data['password']

        existing_user = User.objects(email=email).first()
        if existing_user:
            return {'message': 'User with email already exists.'}, 409

        user = User(email=email, password=password)
        user.save()
        return {'message': 'User created successfully.'}, 201

    @jwt_required()
    def put(self, user_id):
        user = User.objects(id=ObjectId(user_id)).first()
        if not user:
            return {'message': 'User not found.'}, 404

        data = User.parser.parse_args()
        user.email = data.get('email', user.email)
        user.password = data.get('password', user.password)
        user.save()
        return {'message': 'User updated successfully.'}, 200

    @jwt_required()
    def delete(self, user_id):
        user = User.objects(id=ObjectId(user_id)).first()
        if not user:
            return {'message': 'User not found.'}, 404

        user.delete()
        return {'message': 'User deleted successfully.'}, 200
