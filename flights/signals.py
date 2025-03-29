from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Reservation, Flight

@receiver(post_save, sender=Reservation)
def decrement_available_seats(sender, instance, created, **kwargs):
    """
    When a Reservation is made, decrement the available_seats for the associated Flight.
    """
    if created:
        flight = instance.flight
        flight.available_seats = Flight.objects.select_for_update().get(id=flight.id).available_seats - 1
        flight.save()

@receiver(post_delete, sender=Reservation)
def increment_available_seats(sender, instance, **kwargs):
    """
    When a Reservation is deleted, increment the available_seats for the associated Flight.
    """
    flight = instance.flight
    flight.available_seats = Flight.objects.select_for_update().get(id=flight.id).available_seats + 1
    flight.save()


