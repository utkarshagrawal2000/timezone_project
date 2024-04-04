# from rest_framework.test import APITestCase, force_authenticate
# from rest_framework.authtoken.models import Token
# from django.contrib.auth import get_user_model
# from django.urls import reverse
# from rest_framework import status
# from datetime import datetime
# import pytz
# from rest_framework_simplejwt.tokens import RefreshToken
# from app.models import Booking,Room,Hotel
# from app.serializers import BookingSerializer
# from django.core.cache import cache  # Import cache module
# from account.views import UserRegistrationView, UserLoginView
# from rest_framework.test import APIRequestFactory
# from rest_framework.decorators import authentication_classes, permission_classes



# User = get_user_model()
# def get_tokens_for_user(user):
#   refresh = RefreshToken.for_user(user)
#   return str(refresh.access_token)
  
# class BookingViewsTestCase(APITestCase):

#     def setUp(self):
#         # Disable caching before each test
#         cache.clear()
#          # Create a test user and authenticate
#         self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123',mobile='999999999',tc='1',is_admin=True)
#         self.token = get_tokens_for_user(self.user)
#         # Create a test room
#         self.hotel = Hotel.objects.create(name='Test hotel', location='test',city='testcity',description='Test description',owner=self.user)
#         self.room = Room.objects.create(hotel=self.hotel, room_number=10)
#         print(self.room)

#     # def test_get_bookings(self):
#     #     # Create some sample Booking instances
#     #     booking_data = [
#     #         {'rooms': self.room, 'start_time': datetime(2024, 2, 16, 9, 0, tzinfo=pytz.utc), 'end_time': datetime(2024, 2, 16, 10, 0, tzinfo=pytz.utc)},
#     #         {'rooms': self.room, 'start_time': datetime(2024, 2, 17, 10, 0, tzinfo=pytz.utc), 'end_time': datetime(2024, 2, 17, 11, 0, tzinfo=pytz.utc)},
#     #     ]
#     #     for data in booking_data:
#     #         Booking.objects.create(**data)

#     #     url = reverse('booking-list-create')
        
#     #     # Set the desired timezone in the request header
#     #     headers = {
#     #         'HTTP_USER_TIMEZONE': 'America/New_York',
#     #         'HTTP_AUTHORIZATION': f'Bearer {self.token}'
#     #     }

#     #     print("Request Headers:", headers)

#     #     response = self.client.get(url, **headers)
        
#     #     print("Response Status Code:", response.status_code)
#     #     print("Response Data:", response.data)

#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)
#     #     # Verify that the response contains the bookings in the correct representation for the specified timezone
#     #     self.assertEqual(len(response.data), 2)  # Assuming there are 2 bookings
#     #     # You may want to perform more detailed assertions on the response data

#     def test_create_booking(self):
#         url = reverse('create_booking')
#         # Set the desired timezone in the request header
#         headers = {'HTTP_USER_TIMEZONE': 'America/New_York',
#             'HTTP_AUTHORIZATION': f'Bearer {self.token}'
#         }
#         data = {'rooms': self.room.id, 'start_time': '2024-02-18T09:00', 'end_time': '2024-02-18T10:00','payment_mode':'cash'}
#         print(data,'sfsf')
#         response = self.client.post(url, data, format='json', **headers)
#         print(response.data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         # Verify that the booking was created successfully
#         self.assertEqual(Booking.objects.count(), 1)
#         new_booking = Booking.objects.first()
#         print(new_booking,'jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj')
#         self.assertEqual(new_booking.rooms, self.room)
#         # You may want to perform more detailed assertions on the created booking


# @authentication_classes([])  # No authentication required
# @permission_classes([])  
# class RegistrationLoginTestCase(APITestCase):
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123',mobile='999999999',tc='1',is_admin=True)
#         self.token = get_tokens_for_user(self.user)

#     def test_user_registration(self):
#         url = reverse('register')
#         data = {"username": "testuser1", "email": "test1@example.com", "password": "password123", "password2": "password123", "mobile": "999999996", "tc": "1", "is_admin": "true"}
#         request = self.factory.post(url, data, format='json')
#         response = UserRegistrationView.as_view()(request)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertTrue('token' in response.data)

#     def test_user_login(self):
#         url = reverse('login')
#         data = {'email': 'test@example.com', 'password': 'password123'}
#         request = self.factory.post(url, data, format='json')
#         response = UserLoginView.as_view()(request)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue('token' in response.data)