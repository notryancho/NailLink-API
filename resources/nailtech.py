from flask import jsonify, request
from flask_restful import Resource
from mongoengine.errors import DoesNotExist, ValidationError
from models.nailtech import NailTech

class NailTech(Resource):
    def get(self, nail_tech_id=None):
        if nail_tech_id:
            try:
                nail_tech = NailTech.objects.get(id=nail_tech_id)
            except (DoesNotExist, ValidationError):
                return {"message": "NailTech not found"}, 404
            return jsonify(nail_tech)
        else:
            nail_techs = NailTech.objects.all()
            return jsonify(nail_techs)

    def post(self):
        body = request.get_json()
        nail_tech = NailTech(**body)
        nail_tech.save()
        return jsonify(nail_tech)

    def put(self, nail_tech_id):
        try:
            nail_tech = NailTech.objects.get(id=nail_tech_id)
        except (DoesNotExist, ValidationError):
            return {"message": "NailTech not found"}, 404

        body = request.get_json()
        nail_tech.update(**body)
        nail_tech.reload()
        return jsonify(nail_tech)

    def delete(self, nail_tech_id):
        try:
            nail_tech = NailTech.objects.get(id=nail_tech_id)
        except (DoesNotExist, ValidationError):
            return {"message": "NailTech not found"}, 404

        nail_tech.delete()
        return {"message": "NailTech deleted"}