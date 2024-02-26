from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.test import TestCase
from datetime import datetime
import pytz
from app.models import Booking
from app.serializers import BookingSerializer
from django.core.cache import cache  # Import cache module


class BookingViewsTestCase(APITestCase):

    def setUp(self):
        # Disable caching before each test
        cache.clear()


    def test_get_bookings(self):
        # Create some sample Booking instances
        booking_data = [
            {'room': 'Room 101', 'start_time': datetime(2024, 2, 16, 9, 0, tzinfo=pytz.utc), 'end_time': datetime(2024, 2, 16, 10, 0, tzinfo=pytz.utc)},
            {'room': 'Room 102', 'start_time': datetime(2024, 2, 17, 10, 0, tzinfo=pytz.utc), 'end_time': datetime(2024, 2, 17, 11, 0, tzinfo=pytz.utc)},
        ]
        for data in booking_data:
            Booking.objects.create(**data)

        url = reverse('booking-list-create')
        # Set the desired timezone in the request header
        headers = {'HTTP_USER_TIMEZONE': 'America/New_York'}
        response = self.client.get(url, **headers)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify that the response contains the bookings in the correct representation for the specified timezone
        self.assertEqual(len(response.data), 2)  # Assuming there are 2 bookings
        # You may want to perform more detailed assertions on the response data

    def test_create_booking(self):
        url = reverse('create_booking')
        # Set the desired timezone in the request header
        headers = {'HTTP_USER_TIMEZONE': 'America/New_York'}
        data = {'room': 'Room 103', 'start_time': '2024-02-18T09:00', 'end_time': '2024-02-18T10:00'}
        response = self.client.post(url, data, format='json', **headers)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verify that the booking was created successfully
        self.assertEqual(Booking.objects.count(), 1)
        new_booking = Booking.objects.first()
        self.assertEqual(new_booking.room, 'Room 103')
        # You may want to perform more detailed assertions on the created booking

