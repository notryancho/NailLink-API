from flask import jsonify, request, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, create_access_token
from mongoengine.errors import DoesNotExist, ValidationError
from models.customer import Customer
from models.user import User

class AllCustomers(Resource):
    def get(self):
        customer = Customer.objects.all()
        return jsonify(customer)

class SingleCustomer(Resource):
    def get(self, id):
        customer = Customer.objects(id=id).first()
        if customer:
            return make_response(jsonify(customer=customer))
        return {"message": "Customer not found"}, 404

    def put(self, id):
        customer = Customer.objects(id=id).first()
        if customer:
            body = request.get_json()
            customer.update(**body)
            return make_response(jsonify(customer=customer))
        return {"message": "Customer not found"}, 404

    def delete(self, id):
        customer = Customer.objects(id=id).first()
        if customer:
            customer.delete()
            return {"message": "Customer deleted"}, 204
        return {"message": "Customer not found"}, 404


