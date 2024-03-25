from django.db import models
from django.contrib.auth.models import User
import json
import os

from attendance_system.settings import BASE_DIR 

# UserProfile:
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=255, null=True)
    image = models.ImageField(upload_to='path/to/upload', blank=True, null=True)


# BiometricData: 
class BiometricData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    facial_encoding = models.TextField(null=True, blank=True)  # This will store the encoding as a JSON string
    
    def set_encoding(self, encoding_list):
        self.facial_encoding = json.dumps(encoding_list)
    def get_encoding(self):
        if self.facial_encoding:
            return json.loads(self.facial_encoding)
        return None

# AttendanceRecord:
class AttendanceRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    authentication_method = models.CharField(max_length=50, choices=[
        ('facial', 'Facial Recognition'),
    ])
    PENDING = 'P'
    VERIFIED = 'V'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (VERIFIED, 'Verified'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)

    class Meta:
        unique_together = ['user', 'date'] 