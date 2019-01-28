from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    isDriver = models.BooleanField(default=False)
    vehicle_id = models.CharField(max_length=20, default='')
    vehicle_max_passenger = models.IntegerField(default=4)
    def __str__(self):
        return self.user.username

def create_user_info(sender, **kwargs):
    if kwargs['created']:
        user_info = UserInfo.objects.create(user=kwargs['instance'])

class Ride(models.Model):
    user = models.ManyToManyField(User)
    destination = models.CharField(max_length=100, default='')
    arrival_time = models.CharField(max_length=100, default='20')
    number_passenger = models.IntegerField(default='1')
    vehicle_type = models.CharField(max_length=100, default='')
    isPicked = models.BooleanField(default=False)
    isFinished = models.BooleanField(default=False)
    driver_id = models.IntegerField(default='0')
    passenger_id = models.IntegerField(default='0')
    def __str__(self):
        return str(self.id)

def create_ride(sender, **kwargs):
    if kwargs['created']:
        user_info = Ride.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)
#post_save.connect(create_user_info, sender=User)
#post_save.connect(create_ride, sender=User)
