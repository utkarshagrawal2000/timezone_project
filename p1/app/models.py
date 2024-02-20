from django.db import models

class Booking(models.Model):
    room = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()