from django.db import models
from accounts.models import User

class Matches(models.Model):
    user_id_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_user1')
    user_id_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_user2')
    compatibility_score = models.DecimalField(max_digits=5, decimal_places=2)
    matched_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('blocked', 'Blocked')]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        db_table = 'Matches'
        unique_together = ('user_id_1', 'user_id_2')

class Messages(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = 'Messages'