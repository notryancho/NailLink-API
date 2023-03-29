from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask import jsonify, request
from flask_restful import Resource
from mongoengine.errors import DoesNotExist, ValidationError
from app. import Customer as CustomerModel

class Customer(Resource):
    def get(self, customer_id=None):
        if customer_id:
            try:
                customer = CustomerModel.objects.get(id=customer_id)
            except (DoesNotExist, ValidationError):
                return {"message": "Customer not found"}, 404
            return jsonify(customer)
        else:
            customers = CustomerModel.objects.all()
            return jsonify(customers)

    def post(self):
        body = request.get_json()
        customer = CustomerModel(**body)
        customer.save()
        return jsonify(customer)

    def put(self, customer_id):
        try:
            customer = CustomerModel.objects.get(id=customer_id)
        except (DoesNotExist, ValidationError):
            return {"message": "Customer not found"}, 404

        body = request.get_json()
        customer.update(**body)
        customer.reload()
        return jsonify(customer)

    def delete(self, customer_id):
        try:
            customer = CustomerModel.objects.get(id=customer_id)
        except (DoesNotExist, ValidationError):
            return {"message": "Customer not found"}, 404

        customer.delete()
        return {"message": "Customer deleted"}
