from rest_framework import serializers
from .models import Flight, Reservation

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ['id', 'flight_number', 'departure_city', 'arrival_city', 'departure_time', 'arrival_time', 'price', 'available_seats']

class ReservationSerializer(serializers.ModelSerializer):
    flight_details = FlightSerializer(source='flight', read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'user', 'flight', 'flight_details', 'reservation_date', 'seat_number']
        read_only_fields = ['user', 'reservation_date']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)