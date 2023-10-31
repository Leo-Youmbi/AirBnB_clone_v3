#!/usr/bin/python3
"""API Module for places endpoints"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.user import User
from models.place import Place


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


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_city_places(city_id):
    """
    Retrieves all places in a specific city by ID and returns a JSON response.

    Args:
        city_id (string): The ID of the city to retrieve places from.

    Returns:
        Response: A JSON response containing a list of places in the
        specified city or a 404 error if the city is not found.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city_places = [serialize_to_json(place) for place in city.places]
    return jsonify(city_places)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a specific place by ID and returns a JSON response.

    Args:
        place_id (string): The ID of the place to retrieve.

    Returns:
        Response: A JSON response containing the details of
        the specified place.
    """
    return jsonify(serialize_to_json(storage.get(Place, place_id)))


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a specific place by ID and returns an appropriate JSON response.

    Args:
        place_id (string): The ID of the place to delete.

    Returns:
        Response: A JSON response confirming the deletion or
        a 404 error if the place is not found.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
    Creates a new place in the specified city based on the provided JSON data.

    Args:
        city_id (string): The ID of the city to create the place in.

    Returns:
        Response: A JSON response containing the newly created place
        or an error response if data is invalid or if the city
        or user is not found.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    place_data = request.get_json()
    if not place_data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in place_data:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if 'name' not in place_data:
        return make_response(jsonify({"error": "Missing name"}), 400)

    user_id = place_data['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    place_data['city_id'] = city_id
    new_place = Place(**place_data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """
    Updates a specific place by ID based on the provided JSON data.

    Args:
        place_id (string): The ID of the place to update.

    Returns:
        Response: A JSON response containing the updated place
        or an error response if data is invalid or if the place is not found.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place_data = request.get_json()
    if place_data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    keys_to_ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in place_data.items():
        if key not in keys_to_ignore:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
