
from django.contrib import admin
from django.urls import path,include
from django.conf import settings






urlpatterns = [
    path("admin/", admin.site.urls),
    path('',include('users.urls') ),
    path('flights/', include('flights.urls')),
    path('reviews/', include('reviews.urls'))
]

