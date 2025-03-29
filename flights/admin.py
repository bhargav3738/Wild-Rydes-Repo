from django.contrib import admin
from .models import Flight, Reservation
# Register your models here.
admin.site.register(Flight)
admin.site.register(Reservation)