from django.utils.timezone import make_aware, make_naive
import pytz
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.cache import cache

CACHE_TIMEOUT = 10


@swagger_auto_schema(method='GET', responses={200: BookingSerializer(many=True)})
@api_view(['GET'])
def get_bookings(request):
    """
    Retrieves a list of bookings.
    """
    timezone_name = request.META.get('HTTP_USER_TIMEZONE', 'UTC')  # Get timezone from request headers
    print(timezone_name,'timezone_name')
    # Check cache first
    cache_key = f"bookings_{timezone_name}"
    cached_data = cache.get(cache_key)
    if cached_data:
        print(cached_data)
        return Response(cached_data, status=status.HTTP_200_OK)
    bookings = Booking.objects.all()
    serializer = BookingSerializer(instance=bookings, context={'timezone_name': timezone_name},many=True)
    # Set cache
    cache.set(cache_key, serializer.data, timeout=CACHE_TIMEOUT)
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
        # Clear cache for bookings specific to the timezone
        cache_key = f"bookings_{timezone_name}"
        cache.delete(cache_key)
        return Response({'msg':'created'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
