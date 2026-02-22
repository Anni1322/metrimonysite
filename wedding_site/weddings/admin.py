from django.contrib import admin
from .models import Weddings, Vendors, Wedding_Services, Reviews, Notifications, Admin_Logs

admin.site.register(Weddings)
admin.site.register(Vendors)
admin.site.register(Wedding_Services)
admin.site.register(Reviews)
admin.site.register(Notifications)
admin.site.register(Admin_Logs)