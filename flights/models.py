from django.db import models

class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    airline = models.CharField(max_length=50)
    departure_city = models.CharField(max_length=100)
    arrival_city = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.IntegerField(default=70)

    def __str__(self):
        return f"{self.flight_number}: {self.departure_city} to {self.arrival_city}"
    
    def get_all_seats(self):
        """
        Returns a list of all seat numbers for the flight.
        Example: ['1A', '1B', ..., '30F']
        """
        total_rows = 30  # Total number of rows in the aircraft
        seats_per_row = ['A', 'B', 'C', 'D', 'E', 'F']  # Seats in each row
        all_seats = [f"{row}{seat}" for row in range(1, total_rows + 1) for seat in seats_per_row]
        return all_seats

class Reservation(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE,related_name='reservations')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE,related_name='reservations')
    reservation_date = models.DateTimeField(auto_now_add=True)
    seat_number = models.CharField(max_length=10)
    booked_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('flight', 'seat_number')

    def __str__(self):
        return f"{self.user.username} - {self.flight.flight_number} - Seat {self.seat_number}"
