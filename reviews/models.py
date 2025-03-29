from flightbooking.settings import mongo_db
from datetime import datetime
import pytz
from pymongo.errors import PyMongoError

class Review:
    """
    A class to handle reviews in the MongoDB database.
    """

    collection = mongo_db['flight_db']  # Refers to the 'reviews' collection

    @staticmethod
    def create_review(flight_id, user_id, content):
        """
        Create a new review in the database.

        Args:
            flight_id (str): The ID of the flight being reviewed.
            user_id (str): The ID of the user submitting the review.
            content (str): The review content.

        Returns:
            dict: Result containing the status and review ID or error message.
        """
        if not flight_id or not user_id or not content:
            return {"error": "All fields (flight_id, user_id, content) are required."}

        review = {
            "flight_id": flight_id,
            "user_id": user_id,
            "content": content,
            "created_at": datetime.now(pytz.utc),  # Use timezone-aware datetime
        }

        try:
            result = Review.collection.insert_one(review)
            return {"success": True, "review_id": str(result.inserted_id)}
        except PyMongoError as e:
            return {"error": f"Failed to create review: {str(e)}"}

    @staticmethod
    def get_reviews_by_flight(flight_id):
        """
        Fetch all reviews for a specific flight.

        Args:
            flight_id (str): The flight ID.

        Returns:
            dict: Result containing reviews or error message.
        """
        if not flight_id:
            return {"error": "Flight ID is required."}

        try:
            reviews = list(Review.collection.find({"flight_id": flight_id}))
            return reviews
        except Exception as e:
            raise ValueError(f"Error fetching reviews: {e}")
    @staticmethod
    def get_reviews_by_user(user_id):
        """
        Fetch all reviews by a specific user.

        Args:
            user_id (str): The user ID.

        Returns:
            dict: Result containing reviews or error message.
        """
        if not user_id:
            return {"error": "User ID is required."}

        try:
            reviews = list(Review.collection.find({"user_id": user_id}))
            for review in reviews:
                review["_id"] = str(review["_id"])  # Convert ObjectId to string
            return {"success": True, "reviews": reviews}
        except PyMongoError as e:
            return {"error": f"Failed to fetch reviews: {str(e)}"}
