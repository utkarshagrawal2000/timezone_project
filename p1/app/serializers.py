from rest_framework import serializers
from datetime import datetime
import pytz
from .models import Booking, Hotel, Room, Image, Rating

from drf_yasg.utils import swagger_auto_schema


# class BookingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Booking
#         fields = ['id', 'room', 'start_time', 'end_time']
#     def to_representation(self, instance):
#         print(self.fields['start_time'],'self')
#         timezone_name = self.context.get('timezone_name', 'UTC')
#         self.fields['start_time'] = serializers.DateTimeField(default_timezone=pytz.timezone(timezone_name))
#         self.fields['end_time'] = serializers.DateTimeField(default_timezone=pytz.timezone(timezone_name))
#         return super().to_representation(instance)
    
#     def to_internal_value(self, instance):
#         data = super().to_internal_value(instance)
#         print(self)
#         print('******************************')
#         print(instance['end_time'],'instance')
#         ds=datetime.strptime(instance['start_time'], '%Y-%m-%dT%H:%M')
#         de=datetime.strptime(instance['end_time'], '%Y-%m-%dT%H:%M')
#         timezone_name = self.context.get('timezone_name', 'UTC')

#         user_timezone = pytz.timezone(timezone_name)
#         print(user_timezone,'user_timezone')
#         localized_sdt = user_timezone.localize(ds)
#         localized_edt = user_timezone.localize(de)
#         data['start_time']=localized_sdt
#         data['end_time']=localized_edt
#         print('******************************')
#         return super().to_internal_value(data)
    
    # def save(self, **kwargs):
    #     start_time = self.validated_data.get('start_time')
    #     end_time = self.validated_data.get('end_time')

    #     # Convert start_time and end_time to UTC
    #     utc_start_time = start_time.astimezone(pytz.utc)
    #     utc_end_time = end_time.astimezone(pytz.utc)

    #     # Update the validated data with UTC values
    #     self.validated_data['start_time'] = utc_start_time
    #     self.validated_data['end_time'] = utc_end_time

    #     return super().save(**kwargs)

class BookingSerializer(serializers.ModelSerializer):
    @swagger_auto_schema(operation_description="Converts Booking instance to a representation suitable for the API response")
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        timezone_name = self.context.get('timezone_name', 'UTC')
        user_timezone = pytz.timezone(timezone_name)
        representation['start_time'] = instance.start_time.astimezone(user_timezone).strftime('%d-%m-%Y %H:%M:%S')
        representation['end_time'] = instance.end_time.astimezone(user_timezone).strftime('%d-%m-%Y %H:%M:%S')
        return representation

    @swagger_auto_schema(operation_description="Converts request data to internal values suitable for saving to the database")
    def to_internal_value(self, data):
        timezone_name = self.context.get('timezone_name', 'UTC')
        print(timezone_name,'timezone_name')
        user_timezone = pytz.timezone(timezone_name)
        print(user_timezone,'user_timezone')
        start_time = user_timezone.localize(datetime.strptime(data['start_time'], '%Y-%m-%dT%H:%M'))
        print(start_time,'start_time')
        end_time = user_timezone.localize(datetime.strptime(data['end_time'], '%Y-%m-%dT%H:%M'))
        print(end_time,'end_time')
        return {'start_time': start_time, 'end_time': end_time, 'room': data['room']}
    
    class Meta:
        model = Booking
        fields = ['id', 'room', 'start_time', 'end_time']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image']

class HotelSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    class Meta:
        model = Hotel
        fields = '__all__'

class TopHotelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['id', 'name', 'overall_rating']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'hotel', 'room_number', 'availability']

    def create(self, validated_data):
        room = Room(**validated_data)
        room.full_clean()  # Trigger model validation
        room.save()
        return room

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.full_clean()  # Trigger model validation
        instance.save()
        return instance


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'hotel', 'user', 'rating', 'review']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError('Rating must be between 1 and 5')
        return value