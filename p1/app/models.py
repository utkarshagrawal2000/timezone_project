from django.db import models
from django.db.models import Avg
from django.core.exceptions import ValidationError

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    description = models.TextField()
    overall_rating = models.FloatField(default=0) 
    owner = models.ForeignKey(
        'account.User', on_delete=models.CASCADE, related_name='hotel_owner')

    def __str__(self):
        return f"{self.name} - {self.city}"
    def update_rating(self):
        # Calculate the average rating for the hotel
        ratings_avg = self.ratings.aggregate(Avg('rating'))['rating__avg']
        # Update the overall rating field of the hotel
        self.overall_rating = ratings_avg or 0
        self.save()
    class Meta:
        # Define unique constraint for combination of name, location, and city
        unique_together = ['name', 'location', 'city']

class Rating(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(
        'account.User', on_delete=models.CASCADE, related_name='user')
    rating = models.IntegerField()
    review = models.CharField(max_length=500,null=True, blank=True)

    def save(self, *args, **kwargs):
        # Call the parent class's save method
        super().save(*args, **kwargs)
        # After saving the rating, update the associated hotel's overall rating
        self.hotel.update_rating()

class Image(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='hotel_images')

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=10)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.hotel.name} - Room {self.room_number}"
    
    def clean(self):
        # Check if a room with the same room_number already exists for this hotel
        existing_room = Room.objects.filter(hotel=self.hotel, room_number=self.room_number).exclude(id=self.id).exists()
        if existing_room:
            raise ValidationError({'room_number': 'This room already exists for this hotel.'})

    
class Booking(models.Model):
    rooms = models.ManyToManyField(Room)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user_timezone = models.CharField(max_length=50,default='UTC')  # Store user's timezone for reference
    is_confirmed = models.BooleanField(default=False)
    payment_mode = models.CharField(max_length=50)  # Field to store payment mode
    payment_status = models.CharField(max_length=50, default='pending')  # Field to track payment status
    payment_transaction_id = models.CharField(max_length=100, null=True, blank=True)  # To store payment transaction ID

    def __str__(self):
        return f"Booking for {self.room} from {self.start_date} to {self.end_date}"