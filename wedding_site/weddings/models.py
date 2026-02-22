from django.db import models
from accounts.models import User, Locations
from django.core.validators import MinValueValidator, MaxValueValidator


class Weddings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    partner_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='partner_weddings')
    wedding_date = models.DateField()
    venue = models.CharField(max_length=255)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    guest_count = models.IntegerField()
    theme = models.CharField(max_length=255)
    STATUS_CHOICES = [('planning', 'Planning'), ('booked', 'Booked'), ('completed', 'Completed')]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='planning')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Weddings'

class Vendors(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    VENDOR_TYPE_CHOICES = [('caterer', 'Caterer'), ('photographer', 'Photographer'), ('venue', 'Venue'), ('planner', 'Planner'), ('florist', 'Florist')]
    vendor_type = models.CharField(max_length=15, choices=VENDOR_TYPE_CHOICES)
    business_name = models.CharField(max_length=255)
    description = models.TextField()
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    location = models.ForeignKey(Locations, on_delete=models.SET_NULL, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'Vendors'

class Wedding_Services(models.Model):
    wedding = models.ForeignKey(Weddings, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendors, on_delete=models.CASCADE)
    service_details = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Wedding_Services'

class Reviews(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    reviewed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    wedding = models.ForeignKey(Weddings, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    reviewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Reviews'

class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    TYPE_CHOICES = [('match', 'Match'), ('message', 'Message'), ('wedding_reminder', 'Wedding Reminder')]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Notifications'

class Admin_Logs(models.Model):
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    details = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Admin_Logs'