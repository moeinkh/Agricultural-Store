from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import User
from .forms import UserEditForm
from django.contrib import messages

# Create your views here.
def profile(request):
    user = User.objects.get(pk=request.user.pk)
    return render(request, 'account/profile.html', {'user': user})

def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'پروفایل با موفقیت تغییر کرد')
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = UserEditForm(instance=request.user)
        return render(request, 'account/edit_profile.html', {'form': form})    