from flask import jsonify, request
from flask_restful import Resource
from mongoengine.errors import DoesNotExist, ValidationError
from models.appointment import Appointment

class Appointments(Resource):
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
        appointment = Appointment(
            customer_id=body['customer_id'],
            nail_tech_id=body['nail_tech_id'],
            appt_date=body['appt_date'],
            appt_time=body['appt_time'],
            service_id=body['service_id'],
            status=body['status']
        )
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


           
