#!/usr/bin/python3
"""API Module for city endpoints"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<string:state_id>/cities', methods=['GET', 'POST'],
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
    elif request.method == 'POST':
        city_data = request.get_json()
        if not city_data:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        if "name" not in city_data:
            return make_response(jsonify({"error": "Missing name"}), 400)
        else:
            city = City(**city_data)
            city.__setattr__(state_id, state_id)
            city.save()
            return jsonify(city.to_dict()), 201

    all_cities = [value.to_dict() for value in state.cities]
    return jsonify(all_cities)


@app_views.route('/cities/<string:city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def city(city_id):
    """
    Gets a city in the given city id

    Keyword arguments:
    city_id -- city id
    Return: json list of the city
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    elif request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == 'PUT':
        city_data = request.get_json()
        if not city_data:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        else:
            city.name = city_data["name"]
            city.save()
            return jsonify(city.to_dict()), 200
    return jsonify(city.to_dict())
