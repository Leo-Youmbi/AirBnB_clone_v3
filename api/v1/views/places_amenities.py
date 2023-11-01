#!/usr/bin/python3
"""API Module for places amenities endpoints"""
import os
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.place import Place
from models.amenity import Amenity


storage_type = os.getenv("HBNB_TYPE_STORAGE")


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


@app_views.route('/places/<string:place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_places_amenities(place_id):
    """
    Retrieves amenities associated with a specific place by ID
    and returns a JSON response.

    Args:
        place_id (string): The ID of the place to retrieve amenities from.

    Returns:
        Response: A JSON response containing a list of amenities for the
        specified place or a 404 error if the place is not found.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if storage_type is 'db':
        place_amenities = [
            serialize_to_json(amenity) for amenity in place.amenities
            ]
    else:
        place_amenities = [
            serialize_to_json(amenity) for amenity in place.amenity_ids
            ]
    return jsonify(place_amenities), 200


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_places_amenities(place_id, amenity_id):
    """
    Deletes a specific amenity associated with a place by their respective IDs
    and returns an appropriate JSON response.

    Args:
        place_id (string): The ID of the place.
        amenity_id (string): The ID of the amenity to be deleted.

    Returns:
        Response: A JSON response confirming the deletion or
        a 404 error if the place or amenity is not found.
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if storage_type == 'db':
        places_amenities = place.amenities
    else:
        places_amenities = place.amenity_ids
    if amenity not in places_amenities:
        abort(404)
    places_amenities.remove(amenity)
    place.save()
    return jsonify({}), 200


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_amenities_places(place_id, amenity_id):
    """
    Links an amenity to a place based on their respective IDs
    and returns a JSON response.

    Args:
        place_id (string): The ID of the place.
        amenity_id (string): The ID of the amenity to be linked.

    Returns:
        Response: A JSON response confirming the linkage or
        a 404 error if the place or amenity is not found.
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if storage_type == 'db':
        places_amenities = place.amenities
    else:
        places_amenities = place.amenity_ids
    if amenity in places_amenities:
        return jsonify(serialize_to_json(amenity)), 200
    places_amenities.append(amenity)
    place.save()
    return jsonify(serialize_to_json(amenity)), 201
