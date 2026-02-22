from django.contrib import admin
from .models import User, Profile, Preferences, Locations, Location_Preferences, Photos

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Preferences)
admin.site.register(Locations)
admin.site.register(Location_Preferences)
admin.site.register(Photos)