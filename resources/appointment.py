from flask import jsonify, request
from flask_restful import Resource
from mongoengine.errors import DoesNotExist, ValidationError
from models.appointment import Appointment
from datetime import datetime, time

class AllAppointments(Resource):
    def get(self):
        appointments = Appointment.objects.all()
        return jsonify(appointments)
    
    def post(self):
        body = request.get_json()
        appointment = Appointment(
            customer_id=body['customer_id'],
            customer_name=body['customer_name'],
            nail_tech_id=body['nail_tech_id'],
            nail_tech_name=body['nail_tech_name'],
            appt_date=body['appt_date'],
            appt_time=body['appt_time'],
            service_id=body['service_id'],
            service_name=body['service_name'],
            service_price=body['service_price'],
            status=body['status']
        )
        appointment.save()
        return jsonify(appointment)

class SingleAppointment(Resource):
    def get(self, id):
        appointment = Appointment.objects.get(id=id)
        if appointment is None:
                return {"message": "Appointment not found"}, 404
        return jsonify(appointment)

    def put(self, id):
        try:
            appointment = Appointment.objects.get(id=id)
        except (DoesNotExist, ValidationError):
            return {"message": "Appointment not found"}, 404

        body = request.get_json()
        for key, value in body.items():
            setattr(appointment, key, value)

        appointment.save()
        appointment.reload()
        return jsonify(appointment)

    def delete(self, id):
        appointment = Appointment.objects.get(id=id)
        if appointment is None:
            return {"message": "Appointment not found"}, 404
        appointment.delete()
        return {"message": "Appointment deleted successfully"}, 204
