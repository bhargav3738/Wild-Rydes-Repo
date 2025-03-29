from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Review
from flights.models import Flight 
import requests
from django.shortcuts import render, get_object_or_404


from django.shortcuts import get_object_or_404, render
import requests

def booking_view(request, flight_id):
    # Fetch flight details
    flight = get_object_or_404(Flight, id=flight_id)
    
    # Define the API endpoint URL
    api_url = request.build_absolute_uri(f'/reviews/flight/{flight_id}/')
    
    try:
        # Make a GET request to the API endpoint
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad status codes
        reviews = response.json()
        if isinstance(reviews, dict):
            reviews = reviews.get("data", [])  # Adjust based on API structure
    except requests.exceptions.RequestException as e:
        # Handle exceptions (e.g., network issues, API errors)
        reviews = []
        print(f"Error fetching reviews: {e}")
    
    # Fetch available seats (replace with actual logic)
     # Example logic
    
    context = {
        'flight': flight.id,
        'reviews': reviews,
        
    }
    print(context)
  
    return render(request, 'flights/booking.html', context)


class ReviewListView(APIView):
    
    def get(self, request, flight_id=None, user_id=None):
        try:
            if flight_id:
                # Fetch reviews by flight ID
                reviews = Review.get_reviews_by_flight(flight_id)
                
            elif user_id:
                # Fetch reviews by user ID
                reviews = Review.get_reviews_by_user(user_id)
                
            else:
                return Response({'error': 'Invalid query parameters'}, status=status.HTTP_400_BAD_REQUEST)

            # Serialize reviews
            serialized_reviews = [
                {
                    "id": str(review["_id"]),
                    "flight_id": review["flight_id"],
                    "user_id": review["user_id"],
                    "content": review["content"],
                    "created_at": review["created_at"].strftime('%Y-%m-%d %H:%M:%S')  # Format datetime
                }
                for review in reviews
            ]
            return Response(serialized_reviews, status=status.HTTP_200_OK)
        except KeyError as e:
            return Response({'error': f"Missing key: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except TypeError as e:
            return Response({'error': f"Type error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateReviewView(APIView):
    def post(self, request,flight_id):
        data = request.data
        flight_id = flight_id
        user_id = data.get("user_id")
        content = data.get("content")

        if not all([flight_id, user_id, content]):
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        review_id = Review.create_review(flight_id, user_id, content)
        return Response({"message": "Review created", "review_id": str(review_id)}, status=status.HTTP_201_CREATED)
