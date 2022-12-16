#!/usr/bin/python3
"""City objects that handles all default RESTFul API actions"""
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def display_cities(state_id):
    """Display all cities"""
    states = storage.get(State, state_id)
    list_cities = []

    if not states:
        abort(404)
    for city in states.cities:
        list_cities.append(city.to_dict())

    return jsonify(list_cities)


@app_views.route("/cities/<city_id>", methods=["GET"],
                 strict_slashes=False)
def display_city_id(city_id):
    """Return a specific state"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DEL"],
                 strict_slashes=False)
def delete_city(city_id):
    """Delete a specific city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    storage.delete(city)
    storage.save()

    return (jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """create a city"""
    states = storage.get(State, state_id)
    state_data = request.get_json()
    if not states:
        abort(404)
    if not state_data:
        return (jsonify({"error": "Not a JSON"}), 400)
    if "name" not in state_data:
        return (jsonify({"error": "Missing name"}), 400)

    nw_instance = City(**state_data)
    nw_instance.state_id = states.id
    nw_instance.save()

    return (jsonify(nw_instance.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"],
                 strict_slashes=False)
def update_city(city_id):
    """Update a city"""
    city = storage.get(City, city_id)
    city_data = request.get_json()
    ignore = ["id", "state_id", "created_at", "updated_at"]

    if not city:
        abort(404)
    if not city_data:
        return (jsonify({"error": "Not a JSON"}), 400)

    for key, value in city_data.items():
        if key not in ignore:
            setattr(city, key, value)

    storage.save()

    return (jsonify(city.to_dict()), 200)
