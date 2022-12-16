#!/usr/bin/python3
"""State module for the RestAPI"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def display_states():
    """Return the list of the all States"""
    states = storage.all(State).values()
    state_list = []
    for state in states:
        state_list.append(state.to_dict())

    return jsonify(state_list)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def display_state_id(state_id):
    """Return a specific state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete a specific state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    storage.delete(state)
    storage.save()

    return (jsonify({}), 200)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """Create a state"""
    state_data = request.get_json()

    if not state_data:
        return (jsonify({"error": "Not a JSON"}), 400)
    if "name" not in state_data:
        return (jsonify({"error": "Missing name"}), 400)

    nw_intance = State(**state_data)
    nw_intance.save()

    return (jsonify(nw_intance.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """Update a specific State"""
    state = storage.get(State, state_id)
    state_data = request.get_json()
    ignore = ["id", "created_at", "updated_at"]

    if not state:
        abort(404)
    if not state_data:
        return (jsonify({"error": "Not a JSON"}), 400)

    for key, value in state_data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()

    return (jsonify(state.to_dict()), 200)
