#!/usr/bin/python3
"""City objects that handles all default RESTFul API actions"""
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def display_cities():
    """Return the list of the all States"""
    states = storage.all(State).values()
    cities_list = []

    if not states:
        abort(404)
    for city in states.cities:
        cities_list.append(city.to_dict())

    return jsonify(cities_list)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def display_city_id(city_id):
    """Return a specific state"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """Delete a specific state"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    storage.delete(city)
    storage.save()

    return (jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def create_state(state_id):
    """Create a state"""
    state = storage.get(State, state_id)
    state_data = request.get_json()

    if not state_data:
        abort(404)
    if not state_data:
        return (jsonify({"error": "Not a JSON"}), 400)
    if "name" not in state_data:
        return (jsonify({"error": "Missing name"}), 400)

    nw_intance = City(**state_data)
    nw_intance.state_id = state.id
    nw_intance.save()

    return (jsonify(nw_intance.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_state(city_id):
    """Update a specific State"""
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
