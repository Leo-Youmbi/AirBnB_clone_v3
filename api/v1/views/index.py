#!/usr/bin/python3
"""Module for route /status"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def status_view():
    """Returns Successful status"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
def stats_view():
    """Returns statistics of classes in storage"""
    class_stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(class_stats)
