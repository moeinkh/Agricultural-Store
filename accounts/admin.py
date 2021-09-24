from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import User

UserAdmin.fieldsets[1][1]['fields'] = (
                ('first_name', 'last_name', 'email', 'phone', 'specialty'),
)


admin.site.register(User, UserAdmin)