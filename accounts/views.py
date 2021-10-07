from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import User
from orders.models import Order, OrderItem
from .forms import UserEditForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def profile(request):
    user = User.objects.get(pk=request.user.pk)
    return render(request, 'account/profile.html', {'user': user})

@login_required
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

@login_required
def order_list(request):
    order = Order.objects.filter(user=request.user)
    return render(request, 'account/order_list.html', {
        'order': order
    })

@login_required
def order_details(request, id):
    order = get_object_or_404(Order, id=id) 
    return render(request, 'account/order_details.html', {
        'order': order,
    })    