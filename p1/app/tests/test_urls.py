# from rest_framework.test import APITestCase
# from django.urls import reverse,resolve
# from rest_framework import status
# from django.test import TestCase,SimpleTestCase
# from datetime import datetime
# import pytz
# from app.views import get_bookings,create_booking
# from app.serializers import BookingSerializer


# #for class based views we fave to use func.view_class
# class TestUrls(SimpleTestCase):
#     def test_get_bookings_is_resolved(self):
#         url =reverse('booking-list-create')
#         print(resolve(url))
#         self.assertEquals(resolve(url).func,get_bookings)
#     def test_create_bookings_is_resolved(self):
#         url =reverse('create_booking')
#         print(resolve(url))
#         self.assertEquals(resolve(url).func,create_booking)