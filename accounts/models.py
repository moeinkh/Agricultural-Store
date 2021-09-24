from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    phone = models.CharField('شماره موبایل', max_length=11, null=True, blank=True)
    specialty = models.CharField('تخصص', max_length=512, null=True, blank=True)