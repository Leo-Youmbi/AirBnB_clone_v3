#!/usr/bin/python3
"""API Module for places reviews endpoints"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User
from models.place import Place
from models.review import Review


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


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_place_reviews(place_id):
    """
    Retrieves all reviews for a specific place by ID and
    returns a JSON response.

    Args:
        place_id (string): The ID of the place to retrieve reviews from.

    Returns:
        Response: A JSON response containing a list of reviews for the
        specified place or a 404 error if the place is not found.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place_reviews = [serialize_to_json(review) for review in place.reviews]
    return jsonify(place_reviews)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a specific review by ID and returns a JSON response.

    Args:
        review_id (string): The ID of the review to retrieve.

    Returns:
        Response: A JSON response containing the details of
        the specified review.
    """
    return jsonify(serialize_to_json(storage.get(Review, review_id)))


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a specific review by ID and returns an appropriate JSON response.

    Args:
        review_id (string): The ID of the review to delete.

    Returns:
        Response: A JSON response confirming the deletion or
        a 404 error if the review is not found.
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """
    Creates a new review for a specific place based on the provided JSON data.

    Args:
        place_id (string): The ID of the place to create the review for.

    Returns:
        Response: A JSON response containing the newly created review or
        an error response if data is invalid or if the place or
        user is not found.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    review_data = request.get_json()
    if review_data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in review_data:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if 'text' not in review_data:
        return make_response(jsonify({"error": "Missing text"}), 400)

    user_id = review_data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    review_data['place_id'] = place_id
    new_review = Review(**review_data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """
    Updates a specific review by ID based on the provided JSON data.

    Args:
        review_id (string): The ID of the review to update.

    Returns:
        Response: A JSON response containing the updated review or
        an error response if data is invalid or if the review is not found.
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review_data = request.get_json()
    if review_data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    keys_to_ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in review_data.items():
        if key not in keys_to_ignore:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
