from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


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


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieves all users and returns a JSON response.

    Returns:
        Response: A JSON response containing a list of all users.
    """
    all_users = [
        serialize_to_json(user) for user in storage.all(User).values()
        ]
    return jsonify(all_users)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """
    Retrieves a specific user by ID and returns a JSON response.

    Args:
        user_id (string): The ID of the user to retrieve.

    Returns:
        Response: A JSON response containing the details of the specified user.
    """
    return jsonify(serialize_to_json(storage.get(User, user_id)))


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a specific user by ID and returns an appropriate JSON response.

    Args:
        user_id (string): The ID of the user to delete.

    Returns:
        Response: A JSON response confirming the deletion or
        a 404 error if the user is not found.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Creates a new user based on the provided JSON data.

    Returns:
        Response: A JSON response containing the newly created user or
        an error response if data is invalid.
    """
    user_data = request.get_json()
    if not user_data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'email' not in user_data:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if 'password' not in user_data:
        return make_response(jsonify({"error": "Missing password"}), 400)
    new_user = User(**user_data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """
    Updates a specific user by ID based on the provided JSON data.

    Args:
        user_id (string): The ID of the user to update.

    Returns:
        Response: A JSON response containing the updated user or
        an error response if data is invalid or the user is not found.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user_data = request.get_json()
    if not user_data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in user_data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
