from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import User
from products.models import Product
from orders.models import Order, OrderItem
from tickets.models import Ticket, TicketComment
from tickets.forms import TicketCommentCreateForm
from .forms import UserEditForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
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



# ADMIN MANAGEMENT
def admin_panel(request):
    sale = OrderItem.objects.values('order__status', 'product__name').annotate(Sum('quantity'), Sum('total_price')).order_by('-quantity__sum').filter(order__status=2)
    
    return render(request, 'adminlte/admin_panel.html', {
        'sale': sale,
        'open_tickets': Ticket.objects.exclude(status=4),
        'users_count': User.objects.all().count(),
        'product_count': Product.objects.all().count(),
        'orders_count': Order.objects.all().count(),
        'orders': Order.objects.filter(status=1),
    })

def ticket_details_admin_panel(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    ticketcomment = TicketComment.objects.filter(ticket_id=id)

    return render(request, 'adminlte/ticket_details_admin_panel.html', {
        'ticket': ticket,
        'ticketcomment': ticketcomment,
    })
        
def add_ticketcomment_admin(request, id):
    url = request.META.get('HTTP_REFERER')  
    if request.method == 'POST':
        form = TicketCommentCreateForm(request.POST)
        if form.is_valid():
            comment = TicketComment()
            comment.text = form.cleaned_data['text']
            comment.image = form.cleaned_data['image']
            comment.ticket_id = id
            comment.author_id = request.user.id 
            comment.ticket.updated_at = timezone.now()
            comment.save()
            comment.ticket.save()
            messages.success(request, 'جواب با موفقیت ثبت گردید')
            return HttpResponseRedirect(url)
    else:
        form = TicketCommentCreateForm()
    return HttpResponseRedirect(url)
    