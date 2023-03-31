from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from mongoengine.errors import DoesNotExist, ValidationError
from models.customer import Customer

class Customer(Resource):
    @jwt_required()
    def get(self, customer_id=None):
        if customer_id:
            try:
                customer = Customer.objects.get(id=customer_id)
            except (DoesNotExist, ValidationError):
                return {"message": "Customer not found"}, 404
            return jsonify(customer)
        else:
            customers = Customer.objects.all()
            return jsonify(customers)

    @jwt_required()
    def post(self):
        body = request.get_json()
        customer = Customer(**body)
        customer.save()
        return jsonify(customer)

    @jwt_required()
    def put(self, customer_id):
        try:
            customer = Customer.objects.get(id=customer_id)
        except (DoesNotExist, ValidationError):
            return {"message": "Customer not found"}, 404

        body = request.get_json()
        customer.update(**body)
        customer.reload()
        return jsonify(customer)

    @jwt_required()
    def delete(self, customer_id):
        try:
            customer = Customer.objects.get(id=customer_id)
        except (DoesNotExist, ValidationError):
            return {"message": "Customer not found"}, 404

        customer.delete()
        return {"message": "Customer deleted"}

