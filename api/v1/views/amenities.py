#!/usr/bin/python3
"""Amenity objects that handles all default RESTFul API actions"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/amenities", methods=["GET"],
                 strict_slashes=False)
def display_amenities():
    """display all amenities"""
    amenities = storage.all(Amenity).values()
    amenity_list = []
    for amemity in amenities:
        amenity_list.append(amemity.to_dict())

    return jsonify(amenity_list)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def display_amenity_id(amenity_id):
    """Display specific amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not Amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete a specfic amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return (jsonify({}), 200)


@app_views.route("/amenities", methods=["POST"],
                 strict_slashes=False)
def create_amenity():
    """create a amenity"""
    amenity_data = request.get_json()
    if not amenity_data:
        return (jsonify({"error": "Not a JSON"}), 400)
    if "name" not in amenity_data:
        return (jsonify({"error": "Missing name"}), 400)

    nw_intance = Amenity(**amenity_data)
    nw_intance.save()

    return (jsonify(nw_intance.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """update a amaneity"""

    amenity = storage.get(Amenity, amenity_id)
    amenity_data = request.get_json()
    ignore = ["id", "created_at", "updated_at"]

    if not amenity:
        abort(404)
    if not amenity_data:
        return (jsonify({"error": "Not a JSON"}), 400)

    for key, value in amenity_data.items():
        if key not in ignore:
            setattr(amenity, key, value)

    storage.save()

    return (jsonify(amenity.to_dict()), 200)
