from django.contrib import admin
from accounts.models import UserProfile, UserInfo, Ride
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserInfo)
admin.site.register(Ride)
