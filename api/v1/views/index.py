#!/usr/bin/python3
"""Module for route /status"""
from api.v1.views import app_views
from flask import jsonify
import models


@app_views.route('/status', methods=['GET'])
def status_view():
    """Returns Successful status"""
    return jsonify({'status': 'OK'})
