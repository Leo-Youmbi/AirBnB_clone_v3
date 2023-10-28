#!/usr/bin/python3
"""API Module for state"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Returns all the states"""
    all_states = [value.to_dict() for value in storage.all(State).values()]
    return jsonify(all_states)


@app_views.route('states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def state(state_id):
    """Returns the state having the id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    elif request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == 'PUT':
        d = request.get_json()
        if not d:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        state.name = d["name"]
        state.save()
    return jsonify(state.to_dict()), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    else:
        new_state = State(**data)
        new_state.save()
        return jsonify(new_state.to_dict()), 202
