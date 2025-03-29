from django.urls import path
from .views import FlightViewSet, ReservationViewSet
from .views import FlightSearchView,home_view,book_flight,reservations_view,cancel_reservation, booking_view,contributors_view,submit_review

urlpatterns = [
    # Flight endpoints
    path('flight/', FlightViewSet.as_view({'get': 'list'}), name='flight-list'),
    path('flight/<int:pk>/', FlightViewSet.as_view({'get': 'retrieve'}), name='flight-detail'),

    # Reservation endpoints
    path('reservation/', ReservationViewSet.as_view({'get': 'list', 'post': 'create'}), name='reservation-list'),
    path('reservation/<int:pk>/', ReservationViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy',
    }), name='reservation-detail'),
    
    path('flight/search/', FlightSearchView.as_view(), name='flight-search'),
    path('home/', home_view, name='home'),
    path('book/<int:flight_id>/', book_flight, name='book_flight'),
    path('reservations/', reservations_view, name='reservations'),
    path('cancel_reservation/<int:reservation_id>/', cancel_reservation, name='cancel_reservation'),
    path('booking/<int:flight_id>/', booking_view, name='booking_view'),
    path('contributors/', contributors_view, name='contributors'),
    path('submitreview/<int:flight_id>/',submit_review,name ='submit_review')
]