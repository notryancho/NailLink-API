from flask import jsonify, request
from flask_restful import Resource
from mongoengine.errors import DoesNotExist, ValidationError
from models.appointment import Appointment
from datetime import datetime

class SingleAppointment(Resource):
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
        try:
            appt_time_str = body['appt_time']
            appt_time = datetime.strptime(appt_time_str, '%H:%M:%S').time()
        except ValueError:
            return {"message": "Invalid appointment time format, must be in HH:MM:SS format."}, 400

        appointment = Appointment(
            customer_id=body['customer_id'],
            nail_tech_id=body['nail_tech_id'],
            appt_date=body['appt_date'],
            appt_time=appt_time,
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
        for key, value in body.items():
            setattr(appointment, key, value)

        appointment.save()
        appointment.reload()
        return jsonify(appointment)

    def delete(self, appointment_id):
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except (DoesNotExist, ValidationError):
            return {"message": "Appointment not found"}, 404

        appointment.delete()
        return {"message": "Appointment deleted successfully"}, 204



           
