from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import User
from django.forms import TextInput, EmailInput

class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone')
        widgets = {
            'username': TextInput(attrs={'class': 'input', 'placeholder': 'نام کاربری جدید خود را وارد نمایید..'}),
            'email': EmailInput(attrs={'class': 'input', 'placeholder': 'ایمیل جدید خود را وارد نمایید'}),
            'first_name': TextInput(attrs={'class': 'input', 'placeholder': 'نام جدید خود را پارد نمایید...'}),
            'last_name': TextInput(attrs={'class': 'input', 'placeholder': 'نام خانوادگی جدید خود را وارد نمایید..'}),
            'phone': TextInput(attrs={'class': 'input', 'placeholder': 'شماره تلفن جدید خود را وارد نمایید..'}),
        }

        