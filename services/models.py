# services/models.py
from django.db import models
from django.contrib.auth.models import User

class ServiceProvider(models.Model):
    SERVICE_TYPES = [
        ('solar', 'Solar Installation'),
        ('insulation', 'Home Insulation'),
        ('compost', 'Compost Pickup'),
        ('rainwater', 'Rainwater Harvesting'),
    ]
     
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES)
    location = models.CharField(max_length=100)
    certification = models.FileField(upload_to='certifications/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.service_type}"

class Booking(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    booking_date = models.DateField()

    def __str__(self):
        return f"{self.customer.username} booked {self.provider.name}"
