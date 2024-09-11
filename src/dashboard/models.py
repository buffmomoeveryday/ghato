# Create your models here.
# your_app_name/models.py

from django.db import models

from users.models import CustomUser as User
from tenant.models import TenantAwareModel

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    room_name = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.room_name} - {self.timestamp}"
