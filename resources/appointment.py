from flask import jsonify, request
from flask_restful import Resource
from mongoengine.errors import DoesNotExist, ValidationError
from app import Customer, NailTech, Appointment, Review, Service


class AppointmentResource(Resource):
    def get(self, appointment_id=None):
        if appointment_id:
            try:
                appointment = Appointment.objects.get(id=appointment_id)
            except (DoesNotExist, ValidationError):
                return {"message": "Appointment not found"}, 404
            return jsonify(appointment)
        else:
            appointments = Appointment.objects.all()
            return jsonify(appointments)

    def post(self):
        body = request.get_json()
        appointment = Appointment(**body)
        appointment.save()
        return jsonify(appointment)

    def put(self, appointment_id):
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except (DoesNotExist, ValidationError):
            return {"message": "Appointment not found"}, 404

        body = request.get_json()
        appointment.update(**body)
        appointment.reload()
        return jsonify(appointment)

    def delete(self, appointment_id):
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except (DoesNotExist, ValidationError):
            return {"message": "Appointment not found"}, 404

        appointment.delete()
        return {"message": "Appointment deleted successfully"}, 204

        


#         from flask import jsonify, request
# from flask_restful import Resource
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from mongoengine.errors import ValidationError, DoesNotExist
# from datetime import datetime

# from models import Appointment, Customer, NailTech, Service

# class AppointmentListResource(Resource):
#     @jwt_required()
#     def get(self):
#         user_id = get_jwt_identity()
#         customer = Customer.objects(user_id=user_id).first()
#         if not customer:
#             return {"message": "User not found"}, 404
#         appointments = Appointment.objects(customer_id=customer.id)
#         return jsonify(appointments)

#     @jwt_required()
#     def post(self):
#         user_id = get_jwt_identity()
#         customer = Customer.objects(user_id=user_id).first()
#         if not customer:
#             return {"message": "User not found"}, 404

#         data = request.get_json()
#         try:
#             nail_tech = NailTech.objects.get(id=data['nail_tech_id'])
#             service = Service.objects.get(id=data['service_id'])
#             appt_date = datetime.strptime(data['appt_date'], '%Y-%m-%d').date()
#             appt_time = datetime.strptime(data['appt_time'], '%H:%M').time()
#             appointment = Appointment(customer_id=customer.id, nail_tech_id=nail_tech.id,
#                                        appt_date=appt_date, appt_time=appt_time,
#                                        service_id=service.id, status='booked')
#             appointment.save()
#             return jsonify({"message": "Appointment created", "id": str(appointment.id)}), 201
#         except (ValidationError, DoesNotExist) as e:
#             return {"message": str(e)}, 400


# class AppointmentResource(Resource):
#     @jwt_required()
#     def get(self, id):
#         user_id = get_jwt_identity()
#         customer = Customer.objects(user_id=user_id).first()
#         if not customer:
#             return {"message": "User not found"}, 404
#         try:
#             appointment = Appointment.objects.get(id=id, customer_id=customer.id)
#             return jsonify(appointment)
#         except DoesNotExist:
#             return {"message": "Appointment not found"}, 404

#     @jwt_required()
#     def put(self, id):
#         user_id = get_jwt_identity()
#         customer = Customer.objects(user_id=user_id).first()
#         if not customer:
#             return {"message": "User not found"}, 404
#         try:
#             appointment = Appointment.objects.get(id=id, customer_id=customer.id)
#             data = request.get_json()
#             if 'status' in data:
#                 appointment.status = data['status']
#             if 'appt_date' in data:
#                 appointment.appt_date = datetime.strptime(data['appt_date'], '%Y-%m-%d').date()
#             if 'appt_time' in data:
#                 appointment.appt_time = datetime.strptime(data['appt_time'], '%H:%M').time()
#             if 'nail_tech_id' in data:
#                 appointment.nail_tech_id = data['nail_tech_id']
#             if 'service_id' in data:
#                 appointment.service_id = data['service_id']
#             appointment.save()
#             return jsonify({"message": "Appointment updated"}), 200
#         except DoesNotExist:
#             return {"message": "Appointment not found"}, 404

#     @jwt_required()
#     def delete(self, id):
#         user_id = get_jwt_identity()
#         customer = Customer.objects(user_id=user_id).first()
#         if not customer:
#             return {"message": "User not found"}, 404
#         try:
#             appointment = Appointment.objects.get(id=id, customer_id=customer.id)
           
           
