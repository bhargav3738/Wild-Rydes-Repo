from django.urls import path
from .views import ReviewListView, CreateReviewView, booking_view

urlpatterns = [
    # Endpoint for creating a review
    path('create/<str:flight_id>/', CreateReviewView.as_view(), name='create_review'),

    # Endpoint for getting reviews by flight ID
    # path('flight/<str:flight_id>/', ReviewListView.as_view(), name='reviews_by_flight'),
    path('flight/<str:flight_id>/', ReviewListView.as_view(), name='reviews_by_flight'),
    
]