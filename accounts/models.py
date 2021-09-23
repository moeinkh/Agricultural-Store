from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    phone = models.PositiveIntegerField('شماره موبایل')
    specialty = models.CharField('تخصص', max_length=512)