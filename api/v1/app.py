#!/usr/bin/python3
"""app Flask api
"""
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

host = getenv('HBNB_API_HOST') or '0.0.0.0'
port = getenv('HBNB_API_PORT') or 5000

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)

cors = CORS(app, resources={'*': {'origins': '0.0.0.0'}})


@app.teardown_appcontext
def close(self):
    """Close session"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """ Page not found error 404 """
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    app.run(host=host, port=port, threaded=True)
