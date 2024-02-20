# from rest_framework.test import APITestCase
# from django.urls import reverse
# from rest_framework import status
# from django.test import TestCase
# from datetime import datetime
# import pytz
# from app.models import Booking
# from app.serializers import BookingSerializer



# class BookingSerializerTestCase(TestCase):
#     def setUp(self):
#         # Create a Booking instance with some sample data
#         self.booking_data = {
#             'id': 1,
#             'room': 'Room 101',
#             'start_time': datetime(2024, 2, 16, 9, 0, tzinfo=pytz.utc),  # UTC time
#             'end_time': datetime(2024, 2, 16, 10, 0, tzinfo=pytz.utc),    # UTC time
#         }
#         self.booking = Booking.objects.create(**self.booking_data)

#     def test_representation_with_custom_serializer(self):
#         serializer = BookingSerializer(instance=self.booking, context={'timezone_name': 'America/New_York'})
#         representation = serializer.data

#         # Check if start_time and end_time are represented in the correct format
#         self.assertEqual(representation['start_time'], '16-02-2024 04:00:00')  # Converted to America/New_York
#         self.assertEqual(representation['end_time'], '16-02-2024 05:00:00')    # Converted to America/New_York

#     def test_internal_value_with_custom_serializer(self):
#         data = {
#             'room': 'Room 102',
#             'start_time': '2024-02-16T10:00',  # Local time in America/New_York
#             'end_time': '2024-02-16T11:00',    # Local time in America/New_York
#         }

#         serializer = BookingSerializer(data=data, context={'timezone_name': 'America/New_York'})
#         self.assertTrue(serializer.is_valid())
        
#         # Save the object to the database
#         serializer.save()

#         # Retrieve the object from the database
#         new_booking = Booking.objects.get(room='Room 102')

#         # Check if start_time and end_time are saved correctly
#         self.assertEqual(new_booking.start_time, datetime(2024, 2, 16, 10, 0, tzinfo=pytz.utc))  # Converted to UTC
#         self.assertEqual(new_booking.end_time, datetime(2024, 2, 16, 11, 0, tzinfo=pytz.utc))    # Converted to UTC
