#!/usr/bin/python3
"""API Module for amenity endpoints"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities():
    """Gets the list of all Amenity objects"""
    all_amenities = [value.to_dict()
                     for value in storage.all(Amenity).values()]
    return jsonify(all_amenities)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Gets an Amenity objects"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenities():
    """Creates a Amenity"""
    amenity_data = request.get_json()
    if not amenity_data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in amenity_data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_obj = Amenity(**amenity_data)
    new_obj.save()
    return (jsonify(new_obj.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates a Amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity_data = request.get_json()
    if not amenity_data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in amenity_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return (jsonify(amenity.to_dict()), 200)
