from django.utils.timezone import make_aware, make_naive
import pytz
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from drf_yasg import openapi

@swagger_auto_schema(method='GET', responses={200: BookingSerializer(many=True)})
@api_view(['GET'])
def get_bookings(request):
    """
    Retrieves a list of bookings.
    """
    timezone_name = request.META.get('HTTP_USER_TIMEZONE', 'UTC')  # Get timezone from request headers
    print(timezone_name,'timezone_name')
    bookings = Booking.objects.all()
    serializer = BookingSerializer(instance=bookings, context={'timezone_name': timezone_name},many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(method='POST', request_body=BookingSerializer, responses={201: openapi.Response('Created')},
                     manual_parameters=[
                         openapi.Parameter('HTTP_USER_TIMEZONE', openapi.IN_HEADER, description="User's timezone", type=openapi.TYPE_STRING)
                     ])
@api_view(['POST'])
def create_booking(request):
    """
    Creates a new booking.
    """
    data = request.data
    timezone_name = request.META.get('HTTP_USER_TIMEZONE', 'UTC')  # Get timezone from request headers
    print('Received timezone:', timezone_name)
    
    serializer = BookingSerializer(data=data, context={'timezone_name': timezone_name})
    if serializer.is_valid():
        print(serializer.validated_data)
        serializer.save()
        return Response({'msg':'created'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @api_view(['POST'])
# def create_booking(request):
#     print('Request headers:', request.headers)
#     data = request.data
#     timezone_name = request.META.get('HTTP_USER_TIMEZONE', 'UTC')  # Get timezone from request headers
#     print('Received timezone:', timezone_name)
#     user_timezone = pytz.timezone(timezone_name)
#     start_time=data['start_time']
#     end_time=data['end_time']
#     # Convert string to datetime object
#     sdt = datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
#     localized_sdt = user_timezone.localize(sdt)
#     edt = datetime.strptime(end_time, '%Y-%m-%dT%H:%M')
#     localized_edt = user_timezone.localize(edt)

#     print(localized_sdt,'localized_sdt')
#     print(localized_edt,'localized_edt')
#     # Convert start_time and end_time to UTC
#     utc_start_time = localized_sdt.astimezone(pytz.utc)
#     utc_end_time = localized_edt.astimezone(pytz.utc)

#     print(utc_start_time,'utc_start_time')
#     print(utc_end_time,'utc_end_time')
#     serializer = BookingSerializer(data={**data, 'start_time': utc_start_time, 'end_time': utc_end_time})
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
