#!/usr/bin/python3
"""User object that handles all default RESTFul API actions"""
from models import storage
from models.user import User
from models.city import City
from models.place import Place
from api.v1.views import app_views
from flasgger.utils import swag_from
from flask import jsonify, abort, request


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
@swag_from("documentation/place/display_place.yml", methods=["GET"])
def display_place(city_id):
    """Display all palces"""
    city = storage.get(City, city_id)
    place_list = []

    if not city:
        abort(404)

    for place in city.places:
        place_list.append(place.to_dict())

    return jsonify(place_list)


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
@swag_from("documentation/place/display_place_id.yml", methods=["GET"])
def display_place_id(place_id):
    """Display a specific place"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
@swag_from("documentation/place/delete_place.yml", methods=["DELETE"])
def delete_place(place_id):
    """Delete a specific place"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    storage.delete(place)
    storage.save()

    return (jsonify({}), 200)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
@swag_from("documentation/place/create_place.yml", methods=["POST"])
def create_place(city_id):
    """Create a specific place"""
    city = storage.get(City, city_id)
    city_data = request.get_json()

    if not city:
        abort(404)

    if not city_data:
        return (jsonify({"error": "Not a JSON"}), 400)
    if "user_id" not in city_data:
        return (jsonify({"error": "Missing user_id"}), 400)

    user = storage.get(User, city_data["user_id"])
    if not user:
        abort(404)
    if "name" not in city_data:
        return (jsonify({"error": "Missing name"}), 400)

    city_data["city_id"] = city_id
    nw_intance = Place(**city_data)
    nw_intance.save()

    return (jsonify(nw_intance.to_dict()), 201)


@ app_views.route("/places/<place_id>", methods=["PUT"],
                  strict_slashes=False)
@ swag_from("documentation/place/update_place.yml", methods=["PUT"])
def update_place(place_id):
    """Update a specific place"""
    place = storage.get(Place, place_id)
    place_data = request.get_json()
    ignore = ["id", "user_id", "city_id", "created_at", "updated_at"]

    if not place:
        abort(404)
    if not place_data:
        return (jsonify({"error": "Not a JSON"}), 400)

    for key, value in place_data.items():
        if key not in ignore:
            setattr(place, key, value)

    storage.save()

    return (jsonify(place.to_dict()), 200)
