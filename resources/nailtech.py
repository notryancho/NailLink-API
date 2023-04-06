from flask import jsonify, request, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from mongoengine.errors import DoesNotExist, ValidationError
from models.nailtech import NailTech

class AllNailTechs(Resource):
    def get(self):
        nail_techs = NailTech.objects.all()
        return jsonify(nail_techs)

class SingleNailTech(Resource):
    def get(self, id):
        nail_tech = NailTech.objects(id=id).first()
        if nail_tech:
            return make_response(jsonify(nail_tech=nail_tech))
        return {"message": "NailTech not found"}, 404

    def put(self, id):
        nail_tech = NailTech.objects(id=id).first()
        if nail_tech:
            body = request.get_json()
            nail_tech.update(**body)
            return make_response(jsonify(nail_tech=nail_tech))
        return {"message": "NailTech not found"}, 404

    def delete(self, id):
        nail_tech = NailTech.objects(id=id).first()
        if nail_tech:
            nail_tech.delete()
            return {"message": "NailTech deleted"}, 204
        return {"message": "NailTech not found"}, 404
