from django.contrib import admin
from .models import CommunityBiodata
from .models import SuccessStory


@admin.register(CommunityBiodata)
class CommunityBiodataAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'full_name', 'gotra', 'deity_number', 'contact_display')
    search_fields = ('full_name', 'serial_number', 'gotra')

    def contact_display(self, obj):
        # This mimics the "Contact Admin" logic for the list view
        return "Contact Admin"
    contact_display.short_description = "Mobile"
    


@admin.register(SuccessStory)
class SuccessStoryAdmin(admin.ModelAdmin):
    list_display = ('couple_name', 'wedding_date', 'is_verified')
    list_filter = ('is_verified',)    