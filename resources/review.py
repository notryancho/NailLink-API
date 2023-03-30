from flask import jsonify, request
from flask_restful import Resource
from mongoengine import DoesNotExist, ValidationError

from models import Review


class ReviewResource(Resource):
    def get(self, review_id=None):
        if review_id:
            try:
                review = Review.objects.get(id=review_id)
            except (DoesNotExist, ValidationError):
                return {"message": "Review not found"}, 404
            return jsonify(review)
        else:
            reviews = Review.objects.all()
            return jsonify(reviews)

    def post(self):
        body = request.get_json()
        review = Review(**body)
        review.save()
        return jsonify(review)

    def put(self, review_id):
        try:
            review = Review.objects.get(id=review_id)
        except (DoesNotExist, ValidationError):
            return {"message": "Review not found"}, 404

        body = request.get_json()
        review.update(**body)
        review.reload()
        return jsonify(review)

    def delete(self, review_id):
        try:
            review = Review.objects.get(id=review_id)
        except (DoesNotExist, ValidationError):
            return {"message": "Review not found"}, 404

        review.delete()
        return {"message": "Review deleted successfully"}, 200
