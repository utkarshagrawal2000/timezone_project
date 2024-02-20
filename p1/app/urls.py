from django.urls import path
from .views import get_bookings,create_booking

urlpatterns = [
    path('get_bookings/', get_bookings, name='booking-list-create'),
    path('create_booking/', create_booking, name='create_booking'),
]