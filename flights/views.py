from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Flight, Reservation
from .serializers import FlightSerializer, ReservationSerializer
from django.db import transaction
from .models import Flight
from .serializers import FlightSerializer
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from users.models import User
#write the contributers
# views.py
import requests
from django.shortcuts import render



def contributors_view(request):
    contributors = [
        {
            "name": "Bhargav Nimbalkar",
            "description": "Lead Backend Developer responsible for Frontend and backend architecture.Responsible for developing CI/CD pipeline and managing AWS infrastructure aswell"
        },
        
        
        
    ]
    return render(request, 'flights/contact.html', {'contributors': contributors})

# @login_required
def reservations_view(request):
    user = request.user
    reservations = Reservation.objects.filter(user=user).select_related('flight')
    context = {'reservations': reservations}
    return render(request, 'flights/reservations.html', context)


def get_username_by_id(user_id):
    try:
        user = User.objects.get(id=user_id)
        return user.username
    except User.DoesNotExist:
        # Handle the case where a user with this ID doesn't exist
        return None

@login_required
def submit_review(request, flight_id):
    if request.method == 'POST':
        user_id = request.user.id
        content = request.POST.get('content', '').strip()
        
        # Validate that content is provided
        if not content:
            messages.error(request, "Review content cannot be empty.")
            return redirect('reservations')

        # Prepare the data to send to the API
        data = {
            "flight_id": str(flight_id),
            "content": content,
            "user_id": user_id
        }

        # Make a POST request to the create review endpoint
        api_url = request.build_absolute_uri(f'/reviews/create/{flight_id}/')
        response = requests.post(api_url, json=data)

        if response.status_code == 201:
            # Successfully created the review
            messages.success(request, "Your review has been submitted successfully!")
            return redirect('reservations')
        else:
            # There was an error, parse the response to get more info
            try:
                error_data = response.json()
                error_message = error_data.get('error', 'An unexpected error occurred.')
            except Exception:
                error_message = 'An unexpected error occurred.'
            
            messages.error(request, error_message)
            return redirect('reservations')
    else:
        # If not a POST request, just redirect or show the relevant page.
        return redirect('reservations')


@login_required
def booking_view(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    all_seats = flight.get_all_seats()
    reserved_seats = Reservation.objects.filter(flight=flight).values_list('seat_number', flat=True)
    available_seats = [seat for seat in all_seats if seat not in reserved_seats]
    api_url = request.build_absolute_uri(f'/reviews/flight/{flight_id}/')
    response = requests.get(api_url)
    
    user =request.user
    
    if response.status_code == 200:
        reviews_data = response.json()
        for review in reviews_data:
            id =review.get('user_id')
            if(id == 'None'):
                review['username'] = 'Anonymous'
            else:
                username = get_username_by_id(id)
                review['username'] = username

    else:
        reviews_data = []

    # Add reviews to the context
    context = {
        'flight': flight,
        'reviews': reviews_data,
        'seats': available_seats
    }
    if request.method == 'POST':
        seat = request.POST.get('seat')

        if not seat:
            messages.error(request, "Please select a seat.")
            return render(request, 'flights/booking.html',context)
        
        if seat in reserved_seats:
            messages.error(request, "Selected seat is already booked. Please choose another seat.")
            return render(request, 'flights/booking.html', context)

        try:
            with transaction.atomic():
                # Double-check seat availability within the transaction
                if Reservation.objects.filter(flight=flight, seat_number=seat).exists():
                    messages.error(request, "Selected seat is already booked. Please choose another seat.")
                    return render(request, 'flights/booking.html',context)

                # Create reservation
                Reservation.objects.create(
                    user=request.user,
                    flight=flight,
                    seat_number=seat,
                    booked_at=timezone.now()
                )
        except Exception as e:
            messages.error(request, "An error occurred while booking your seat. Please try again.")
            print(e)
            return render(request, 'flights/booking.html',context)

        messages.success(request, f"Seat {seat} on flight {flight.flight_number} has been successfully booked.")
        return redirect('reservations')
    

    return render(request, 'flights/booking.html', context)
@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, 'Reservation cancelled successfully.')
        return redirect('reservations')
    return render(request, 'flights/cancel_reservation.html', {'reservation': reservation})
@login_required
def home_view(request):
    departure_city = request.GET.get('departure', '').strip()
    destination_city = request.GET.get('destination', '').strip()
    date = request.GET.get('date', '').strip()

    filters = {}
    if departure_city:
        filters['departure_city__icontains'] = departure_city
    if destination_city:
        filters['arrival_city__icontains'] = destination_city
    if date:
        filters['departure_time__date'] = date

    flights = Flight.objects.filter(**filters)

    context = {'flights': flights}
    return render(request, 'flights/home.html', context)


class FlightSearchView(APIView):
    """
    Handles dynamic search for flights based on departure and arrival cities.
    """

    def get(self, request):
        departure_city = request.query_params.get('departure_city', '').strip()
        arrival_city = request.query_params.get('arrival_city', '').strip()

        # Filter flights based on user input
        flights = Flight.objects.all()
        if departure_city:
            flights = flights.filter(departure_city__icontains=departure_city)
        if arrival_city:
            flights = flights.filter(arrival_city__icontains=arrival_city)

        # Serialize the filtered flights
        serializer = FlightSerializer(flights, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
    
class FlightViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [permissions.IsAuthenticated]

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        flight_id = request.data.get('flight')
        seat_number = request.data.get('seat_number')

        try:
            flight = Flight.objects.select_for_update().get(id=flight_id)
        except Flight.DoesNotExist:
            return Response({'error': 'Flight not found'}, status=status.HTTP_404_NOT_FOUND)

        if flight.available_seats <= 0:
            return Response({'error': 'No available seats'}, status=status.HTTP_400_BAD_REQUEST)

        if Reservation.objects.filter(flight=flight, seat_number=seat_number).exists():
            return Response({'error': 'Seat already reserved'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        reservation = self.get_object()
        self.perform_destroy(reservation)
        return Response(status=status.HTTP_204_NO_CONTENT)
# views.py
def book_flight(request, flight_id):
    # Implement booking logic here
    pass