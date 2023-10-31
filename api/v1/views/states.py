#!/usr/bin/python3
"""API Module for state"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


def serialize_to_json(obj):
    """
    Serializes the given object to a JSON-compatible dictionary representation.

    Args:
        obj: The object to be serialized.

    Returns:
        dict: A dictionary representing the object in a JSON-compatible format.
             Returns a 404 error response if the object is not found.
    """
    return obj.to_dict() if obj else abort(404)


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Returns all the states"""
    all_states = [
        serialize_to_json(value) for value in storage.all(State).values()
        ]
    return jsonify(all_states)


@app_views.route('states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """Returns the state having the id"""
    return jsonify(serialize_to_json(storage.get(State, state_id)))


@app_views.route('states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a specific state by ID and returns an appropriate JSON response.

    Args:
        state_id (string): The ID of the state to delete.

    Returns:
        Response: A JSON response confirming the deletion or
        a 404 error if the state is not found.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """
    Updates a specific state by ID based on the provided JSON data.

    Args:
        state_id (string): The ID of the state to update.

    Returns:
        Response: A JSON response containing the updated state
        or an error response if data is invalid or if the state is not found.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state_data = request.get_json()
    if state_data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    keys_to_ignore = ['id', 'created_at', 'updated_at']
    for key, value in state_data.items():
        if key not in keys_to_ignore:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """post a state"""
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    else:
        new_state = State(**data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201
