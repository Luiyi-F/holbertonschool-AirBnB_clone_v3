#!/usr/bin/python3
"""index file for the RestAPI"""
from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route("/status", strict_slashes=False)
def hbnbstatus(execption):
    """status hbnb"""
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    pass
