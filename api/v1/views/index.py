#!/usr/bin/python3
"""index file for the RestAPI"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage

hbnb_d = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route("/status", strict_slashes=False)
def hbnbStatus():
    """status hbnb"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def hbnbStats():
    """stats hbnb"""
    stats_dict = {}
    for key, value in hbnb_d.items():
        stats_dict[key] = storage.count(value)
    return jsonify(stats_dict)


if __name__ == "__main__":
    pass
