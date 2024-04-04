from django.utils.timezone import make_aware, make_naive
import pytz
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Booking,Hotel,Rating,Image,Room
from .serializers import BookingSerializer,HotelSerializer,RoomSerializer,TopHotelsSerializer,ImageSerializer,RatingSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.cache import cache
from flags.state import flag_enabled
from rest_framework.permissions import BasePermission
from functools import wraps
from rest_framework.views import APIView
from rest_framework import generics
from django.db.models import Avg
from django.core.exceptions import ValidationError
from payments.views import create_payment_order
from django.db import transaction

CACHE_TIMEOUT = 10


@swagger_auto_schema(method='GET', responses={200: BookingSerializer(many=True)})
@api_view(['GET'])

def get_bookings(request):
    if flag_enabled('MY_FEATURE', request=request):
        """
        Retrieves a list of bookings.
        """
        timezone_name = request.META.get('HTTP_USER_TIMEZONE', 'UTC')  # Get timezone from request headers
        print(timezone_name,'timezone_name')
        # Check cache first
        cache_key = f"get:bookings_{timezone_name}"
        cached_data = cache.get(cache_key)
        if cached_data:
            print(cached_data)
            return Response(cached_data, status=status.HTTP_200_OK)
        bookings = Booking.objects.all()
        serializer = BookingSerializer(instance=bookings, context={'timezone_name': timezone_name},many=True)
        # Set cache
        # cache.set(cache_key, serializer.data)
        # cache.set(cache_key, serializer.data, timeout=CACHE_TIMEOUT)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'status':'flag is false'})

@swagger_auto_schema(method='POST', request_body=BookingSerializer, responses={201: openapi.Response('Created')},
                     manual_parameters=[
                         openapi.Parameter('HTTP_USER_TIMEZONE', openapi.IN_HEADER, description="User's timezone", type=openapi.TYPE_STRING)
                     ])
@api_view(['POST'])
def create_booking(request):
    data = request.data
    print(data)
    timezone_name = request.META.get('HTTP_USER_TIMEZONE', 'UTC')
    print('Received timezone:', timezone_name)

    serializer = BookingSerializer(data=data, context={'timezone_name': timezone_name})
    if serializer.is_valid():
        print(serializer.validated_data)
        payment_option = data.get('payment_mode')

        if payment_option == 'pay_later':
            serializer.save(is_confirmed=True, payment_status='pending')

            # Clear cache for bookings specific to the timezone
            cache_key = f"bookings_{timezone_name}"
            cache.delete(cache_key)
            
            return Response({'msg': 'Booking created. Payment pending.'}, status=status.HTTP_201_CREATED)

        elif payment_option == 'cash':
            print(serializer.validated_data,'dddddddddddddwa')

            start_time = serializer.validated_data['start_time']
            end_time = serializer.validated_data['end_time']
            print(start_time,end_time)
            rooms_str = serializer.validated_data['rooms']
            payment_mode = serializer.validated_data['payment_mode']
            print(rooms_str,'fffffffaswsfwesfsegfesf')
            room_ids = [int(room_id) for room_id in rooms_str.split(',') if room_id.strip()]
            print(room_ids,'ffffffffffffffffffffffff')
            # Ensure atomicity of the transaction
            with transaction.atomic():
                booking = Booking.objects.create(
                    start_time=start_time,
                    end_time=end_time,
                    payment_mode=payment_mode,
                    payment_status='completed'  # Assuming payment is already completed for cash mode
                )
                rooms = Room.objects.filter(id__in=room_ids)
                booking.rooms.set(rooms)
            # Clear cache for bookings specific to the timezone
            cache_key = f"bookings_{timezone_name}"
            cache.delete(cache_key)
            
            return Response({'msg': 'Booking created. Payment completed via cash.'}, status=status.HTTP_201_CREATED)

        elif payment_option == 'online':
            payment_transaction_id=create_payment_order(data)  # Implement this method to handle online payment and get transaction ID
            if payment_transaction_id:
                serializer.save(is_confirmed=True, payment_mode='online', payment_status='completed', payment_transaction_id=payment_transaction_id)

                # Clear cache for bookings specific to the timezone
                cache_key = f"bookings_{timezone_name}"
                cache.delete(cache_key)
                
                return Response({'msg': 'Booking created. Online payment completed.'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Online payment failed. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error': 'Invalid payment option.'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class Hotel(APIView):
#     def post(self, request):
#         current_user = request.user
#         user_data = current_user.id
#         # Serialize the request data using HotelSerializer
#         serializer = HotelSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         # Save the serialized data with the associated user ID
#         serializer.save(owner=user_data)
#         return Response({'msg': 'Hotel created Successfully'}, status=status.HTTP_201_CREATED)

class HotelListCreate(generics.ListCreateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class HotelRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class TopHotels(generics.ListAPIView):
    serializer_class = TopHotelsSerializer

    def get_queryset(self):
        city = self.request.query_params.get('city')
        print(city,'dd')
        
        queryset = Hotel.objects.annotate(avg_rating=Avg('ratings__rating'))
        
        # Filter hotels by city
        if city:
            queryset = queryset.filter(city=city)

        # If city is specified, order by average rating within the city, else order by overall rating
        if city:
            queryset = queryset.order_by('-avg_rating')[:10]
        else:
            queryset = queryset.order_by('-overall_rating')[:10]

        return queryset
    
class ImageUpload(generics.CreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def create(self, request, *args, **kwargs):
        hotel_id = self.kwargs.get('hotel_id')
        images_data = request.FILES.getlist('image')  # Get list of uploaded images
        for image_data in images_data:
            serializer = self.get_serializer(data={'image': image_data, 'hotel': hotel_id})
            serializer.is_valid(raise_exception=True)
            serializer.save(hotel_id=hotel_id)  # Ensure hotel_id is passed when saving
        return Response(status=status.HTTP_201_CREATED)

class ImageRetrieve(generics.ListAPIView):
    serializer_class = ImageSerializer
    lookup_url_kwarg = 'hotel_id'
    def get_queryset(self):
        hotel_id = self.kwargs.get(self.lookup_url_kwarg)
        obj=Image.objects.filter(hotel_id=hotel_id)
        print(obj)
        return obj


class RatingListCreate(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class RatingRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class RoomListCreate(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except ValidationError as e:
            return Response({'error': dict(e.message_dict)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save()

class RoomRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer