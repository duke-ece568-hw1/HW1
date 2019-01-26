from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    website = models.URLField(default='')
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

post_save.connect(create_profile, sender=User)
post_save.connect(create_user_info, sender=User)