from flask import jsonify, request
from flask_restful import Resource
from mongoengine.errors import DoesNotExist, ValidationError
from models.service import Service

class AllServices(Resource):
    def get(self):
        services = Service.objects.all()
        return jsonify(services)

class Services(Resource):
    def get(self, service_id=None):
        if service_id:
            try:
                service = Service.objects.get(id=service_id)
            except (DoesNotExist, ValidationError):
                return {"message": "Service not found"}, 404
            return jsonify(service)
        else:
            services = Service.objects.all()
            return jsonify(services)

    def post(self):
        body = request.get_json()
        service = Services(**body)
        service.save()
        return jsonify(service)

    def put(self, service_id):
        try:
            service = Service.objects.get(id=service_id)
        except (DoesNotExist, ValidationError):
            return {"message": "Service not found"}, 404

        body = request.get_json()
        service.update(**body)
        service.reload()
        return jsonify(service)

    def delete(self, service_id):
        try:
            service = Service.objects.get(id=service_id)
        except (DoesNotExist, ValidationError):
            return {"message": "Service not found"}, 404

        service.delete()
        return {"message": "Service deleted successfully"}, 200
