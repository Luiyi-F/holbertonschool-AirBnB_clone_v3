#!/usr/bin/python3
"""User object that handles all default RESTFul API actions"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flasgger.utils import swag_from
from flask import jsonify, abort, request


@app_views.route("/users", methods=["GET"],
                 strict_slashes=False)
@swag_from("/documetation/user/display_users.yml", methods=["GET"])
def display_users():
    """Display all users"""
    users = storage.all(User).values()
    users_list = []

    for user in users:
        users_list.append(user.to_dict())

    return jsonify(users_list)


@app_views.route("/users/<user_id>", methods=["GET"],
                 strict_slashes=False)
@swag_from("/documetation/user/display_user_id.yml", methods=["GET"])
def display_user_id(user_id):
    """Display a specific user"""
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
@swag_from("/documetation/user/delete_user.yml", methods=["DELETE"])
def delete_user(user_id):
    """Delete a specific user"""
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return (jsonify({}), 200)


@app_views.route("/users", methods=["POST"],
                 strict_slashes=False)
@swag_from("/documetation/user/create_user.yml", methods=["POST"])
def create_user():
    """Create a specific user"""
    user_data = request.get_json()

    if not user_data:
        return (jsonify({"error": "Not a JSON"}), 400)
    if "email" not in user_data:
        return (jsonify({"error": "Missing email"}), 400)
    if "password" not in user_data:
        return (jsonify({"error": "Missing password"}), 400)

    nw_intance = User(**user_data)
    nw_intance.save()

    return (jsonify(nw_intance.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
@swag_from("/documetation/user/update_user.yml", methods=["PUT"])
def update_user(user_id):
    """Update a specific user"""
    user = storage.get(User, user_id)
    user_data = request.get_json()
    ignore = ["id", "email", "created_at", "updated_at"]

    if not user:
        abort(404)
    if not user_data:
        return (jsonify({"error": "Not a JSON"}), 400)

    for key, value in user_data.items():
        if key not in ignore:
            setattr(user, key, value)

    storage.save()

    return (jsonify(user.to_dict()), 200)
