from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Create your models here.
class User(AbstractUser):
    USER_TYPE = (
        ('staff', 'staff'),
        ('hospital', 'Hospital'),
        ('patients', 'Patients'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE, default='customer')
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    # Add other common fields like name, address, etc.

class Hospital(models.Model):
    name = models.CharField(max_length=100)
    # Add any additional fields specific to hospitals

class HospitalProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,related_name='hospitalprofile')
    address = models.CharField(max_length= 255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='hospital-profile-pictures')

    def __str__(self):
        return self.user.username

class PatientsProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,related_name='patientsprofile')
    profile_picture = models.ImageField(upload_to='patients-profile-pictures')
    address = models.CharField(max_length= 255, blank=True, null = True)
    
    def __str__(self):
        return self.user.username


