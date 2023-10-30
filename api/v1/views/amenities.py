from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


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


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """
    Retrieves all amenities and returns a JSON response.

    Returns:
        Response: A JSON response containing a list of all amenities.
    """
    all_amenities = [
        serialize_to_json(value) for value in storage.all(Amenity).values()
        ]
    return jsonify(all_amenities)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """
    Retrieves a specific amenity by ID and returns a JSON response.

    Args:
        amenity_id (string): The ID of the amenity to retrieve.

    Returns:
        Response: A JSON response containing the details of
        the specified amenity.
    """
    return jsonify(serialize_to_json(storage.get(Amenity, amenity_id)))


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes a specific amenity by ID and returns an appropriate JSON response.

    Args:
        amenity_id (string): The ID of the amenity to delete.

    Returns:
        Response: A JSON response confirming the deletion or
        a 404 error if the amenity is not found.
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenities():
    """
    Creates a new amenity based on the provided JSON data.

    Returns:
        Response: A JSON response containing the newly created
        amenity or an error response if data is invalid.
    """
    amenity_data = request.get_json()
    if not amenity_data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in amenity_data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_obj = Amenity(**amenity_data)
    new_obj.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    Updates a specific amenity by ID based on the provided JSON data.

    Args:
        amenity_id (string): The ID of the amenity to update.

    Returns:
        Response: A JSON response containing the updated amenity or
        an error response if data is invalid or the amenity is not found.
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity_data = request.get_json()
    if not amenity_data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in amenity_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
