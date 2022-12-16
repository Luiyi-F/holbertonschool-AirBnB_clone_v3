#!/usr/bin/python3
"""Reviews object that handles all default RESTFul API actions"""
from models import storage
from models.user import User
from models.place import Place
from models.review import Review
from api.v1.views import app_views
from flasgger.utils import swag_from
from flask import jsonify, abort, request


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
@swag_from("documentation/reviews/display_reviews.yml", methods=["GET"])
def display_reviews(place_id):
    """Display all reviews"""
    place = storage.get(Place, place_id)
    review_list = []

    if not place:
        abort(404)

    for review in place.reviews:
        review_list.append(review.to_dict())

    return jsonify(review_list)


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
@swag_from("documentation/reviews/display_review_id.yml", methods=["GET"])
def display_review_id(review_id):
    """Display all reviews"""
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
@swag_from("documentation/reviews/delete_review.yml", methods=["DELETE"])
def delete_review(review_id):
    """Display all reviews"""
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    storage.delete(review)
    storage.save()

    return (jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
@swag_from("documentation/reviews/create_review.yml", methods=["POST"])
def create_review(place_id):
    """Display all reviews"""
    place = storage.get(Place, place_id)
    place_data = request.get_json()

    if not place:
        abort(404)

    if not place_data:
        return (jsonify({"error": "Not a JSON"}), 400)
    if "user_id" not in place_data:
        return (jsonify({"error": "Missing user_id"}), 400)

    user = storage.get(User, place_data["user_id"])
    if not user:
        abort(404)
    if "text" not in place_data:
        return (jsonify({"error": "Missing text"}), 400)

    place_data["place_id"] = place_id
    nw_instance = Review(**place_data)
    nw_instance.save()

    return (jsonify(nw_instance.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
@swag_from("documentation/reviews/update_review.yml", methods=["PUT"])
def update_review(review_id):
    """Display all reviews"""
    review = storage.get(Review, review_id)
    review_data = request.get_json()
    ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]

    if not review:
        abort(404)
    if not review_data:
        return (jsonify({"error": "Not a JSON"}), 400)

    for key, value in review_data.items():
        if key not in ignore:
            setattr(review, key, value)

    storage.save()

    return (jsonify(review.to_dict()), 200)
