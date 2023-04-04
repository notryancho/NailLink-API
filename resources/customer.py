from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from mongoengine.errors import DoesNotExist, ValidationError
from models.customer import Customer

class SingleCustomer(Resource):
    
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
        data = request.get_json()
        name = data['name']
        email = data['email']
        password = data['password']
        is_customer = data['is_customer']
        is_nail_tech = data['is_nail_tech']

        existing_user = User.objects(email=email).first()
        if existing_user:
            return {'message': 'User with email already exists.'}, 409

        if is_customer:
            customer = Customer(name=name, email=email, password=password, is_customer=is_customer)
            customer.save()
            access_token = create_access_token(identity=str(customer.id))
        else:
            user = User(name=name, email=email, password=password, is_customer=is_customer, is_nail_tech=is_nail_tech)
            user.save()
            access_token = create_access_token(identity=str(user.id))

        # Return the access token along with the success message
        return {'message': 'User created successfully.', 'access_token': access_token}, 201

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


