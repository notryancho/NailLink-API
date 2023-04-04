from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine.errors import DoesNotExist, ValidationError
from models.nailtech import NailTech
from models.user import User


class SingleNailTech(Resource):

    def get(self, nail_tech_id=None):
        if nail_tech_id:
            try:
                nail_tech = NailTech.objects.get(id=nail_tech_id).to_dict()
            except (DoesNotExist, ValidationError):
                return {"message": "NailTech not found"}, 404
            return jsonify(nail_tech)
        else:
            nail_techs = NailTech.objects.all()
            return jsonify([nail_tech.to_dict() for nail_tech in nail_techs])

    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        current_user = User.objects(id=current_user_id).first()
        if not current_user.is_nail_tech:
            return {"message": "Not authorized to create NailTech profiles"}, 401

        body = request.get_json()
        nail_tech = NailTech(**body)
        nail_tech.save()
        return jsonify(nail_tech.to_dict())

    @jwt_required()
    def put(self, nail_tech_id):
        current_user_id = get_jwt_identity()
        current_user = User.objects(id=current_user_id).first()
        if not current_user.is_nail_tech:
            return {"message": "Not authorized to update NailTech profiles"}, 401

        try:
            nail_tech = NailTech.objects.get(id=nail_tech_id)
        except (DoesNotExist, ValidationError):
            return {"message": "NailTech not found"}, 404

        body = request.get_json()
        nail_tech.update(**body)
        nail_tech.reload()
        return jsonify(nail_tech.to_dict())

    @jwt_required()
    def delete(self, nail_tech_id):
        current_user_id = get_jwt_identity()
        current_user = User.objects(id=current_user_id).first()
        if not current_user.is_nail_tech:
            return {"message": "Not authorized to delete NailTech profiles"}, 401

        try:
            nail_tech = NailTech.objects.get(id=nail_tech_id)
        except (DoesNotExist, ValidationError):
            return {"message": "NailTech not found"}, 404

        nail_tech.delete()
        return {"message": "NailTech deleted"}


