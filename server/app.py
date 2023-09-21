# Import necessary libraries and models
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from models import db, Review

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

db.init_app(app)

# Route to create a new review via POST request
@app.route('/reviews', methods=['POST'])
def create_review():
    data = request.json  # Get JSON data from the request body

    # Extract relevant data for creating a new review
    score = data.get("score")
    comment = data.get("comment")
    user_id = data.get("user_id")
    game_id = data.get("game_id")

    # Create a new review object
    new_review = Review(score=score, comment=comment, user_id=user_id, game_id=game_id)

    # Add the new review to the database
    db.session.add(new_review)
    db.session.commit()

    # Return the newly created review as JSON with a 201 status code (Created)
    response_data = new_review.to_dict()
    return jsonify(response_data), 201

# Route to update an existing review via PATCH request
@app.route('/reviews/<int:id>', methods=['PATCH'])
def update_review(id):
    review = Review.query.get(id)  # Find the review by its ID

    if not review:
        # Return a 404 response if the review doesn't exist
        return jsonify({"error": "Review not found"}), 404

    data = request.json  # Get JSON data from the request body

    # Update the review attributes based on the data in the request
    if "score" in data:
        review.score = data["score"]
    if "comment" in data:
        review.comment = data["comment"]

    # Commit the changes to the database
    db.session.commit()

    # Return the updated review as JSON with a 200 status code (OK)
    response_data = review.to_dict()
    return jsonify(response_data), 200

# Route to delete an existing review via DELETE request
@app.route('/reviews/<int:id>', methods=['DELETE'])
def delete_review(id):
    review = Review.query.get(id)  # Find the review by its ID

    if not review:
        # Return a 404 response if the review doesn't exist
        return jsonify({"error": "Review not found"}), 404

    # Delete the review from the database
    db.session.delete(review)
    db.session.commit()

    # Return a success message as JSON with a 200 status code (OK)
    response_data = {"message": "Review deleted successfully"}
    return jsonify(response_data), 200

if __name__ == '__main__':
    app.run(port=5555)
