from django.urls import path
from .views import get_bookings,create_booking,HotelListCreate,HotelRetrieveUpdateDestroy,TopHotels,\
    ImageUpload,ImageRetrieve,RatingListCreate, RatingRetrieveUpdateDestroy,RoomListCreate,\
    RoomRetrieveUpdateDestroy

urlpatterns = [
    path('get_bookings/', get_bookings, name='booking-list-create'),
    path('create_booking/', create_booking, name='create_booking'),
    path('hotels/', HotelListCreate.as_view(), name='hotel-list-create'),
    path('hotels/<int:pk>/', HotelRetrieveUpdateDestroy.as_view(), name='hotel-retrieve-update-destroy'),
    path('top-hotels/', TopHotels.as_view(), name='top-hotels'),
    path('hotels/<int:hotel_id>/upload-image/', ImageUpload.as_view(), name='image-upload'),
    path('hotels/<int:hotel_id>/images/', ImageRetrieve.as_view(), name='image-retrieve'),
    path('ratings/', RatingListCreate.as_view(), name='rating-list-create'),
    path('ratings/<int:pk>/', RatingRetrieveUpdateDestroy.as_view(), name='rating-retrieve-update-destroy'),
    path('rooms/', RoomListCreate.as_view(), name='room-list-create'),
    path('rooms/<int:pk>/', RoomRetrieveUpdateDestroy.as_view(), name='room-retrieve-update-destroy'),
]