#!/usr/bin/python3
"""API Module for city endpoints"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """
    Gets all the cities in the given state id

    Keyword arguments:
    state_id -- state id
    Return: json list of all the cities in the state
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    all_cities = [value.to_dict() for value in state.cities]
    return jsonify(all_cities)


@app_views.route('/states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_cities(state_id):
    """
    Create a new city record

    Keyword arguments:
    state_id -- state id
    Return: json object of the created city record
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    city_data = request.get_json()
    if not city_data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in city_data:
        return make_response(jsonify({"error": "Missing name"}), 400)

    city = City(**city_data)
    setattr(city, "state_id", state_id)
    print([city.to_dict()])
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """
    Gets a city in the given city id

    Keyword arguments:
    city_id -- city id
    Return: json list of the city
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a city record

    Keyword arguments:
    city_id -- city id
    Return: empty json object
    """

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """
    Updates a city record

    Keyword arguments:
    city_id -- city id
    Return: json object to the updated record
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    city_data = request.get_json()
    if not city_data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    city.name = city_data["name"]
    city.save()
    return jsonify(city.to_dict()), 200
