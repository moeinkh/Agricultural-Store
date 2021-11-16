from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from accounts.models import User
from products.models import Product, Contact
from orders.models import Order, OrderItem
from tickets.models import Ticket, TicketComment
from tickets.forms import TicketCommentCreateForm, TicketCommentCreateAdminForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone

from django.core.mail import send_mail


# Create your views here.

def admin_panel(request):
    sale = OrderItem.objects.values('order__status', 'product__name').annotate(Sum('quantity'), Sum('total_price')).order_by('-quantity__sum').filter(order__status=2)
    
    return render(request, 'adminlte/admin_panel.html', {
        'sale': sale,
        'open_tickets': Ticket.objects.exclude(status=4),
        'users_count': User.objects.all().count(),
        'product_count': Product.objects.all().count(),
        'orders_count': Order.objects.all().count(),
        'orders': Order.objects.filter(status=1),
        'ticket_count': Ticket.objects.all().count(),
        'contact': Contact.objects.all()[:6],
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
            # تنظیمات ارسال فاکتور خرید با ایمیل
            subject = 'جواب شما فرستاده شد'
            message = f'با سلام و خسته نباشید {request.user.username}'
            
            send_mail(subject,
            message,
            'coolgertn@gmail.com', 
            [comment.ticket.user.email], 
            fail_silently=False)

            return HttpResponseRedirect(url)
    else:
        form = TicketCommentCreateForm()
    return HttpResponseRedirect(url)
    
def orders_list_admin(request):
    orders = Order.objects.all()
    return render(request, 'adminlte/order_list_admin.html', {
        'orders': orders,
    })   

def tickets_list_admin(request):
    tickets = Ticket.objects.all()
    return render(request, 'adminlte/tickets_list_admin.html', {
        'tickets': tickets,
    })     

def products_list_admin(request):
    products = Product.objects.all()
    return render(request, 'adminlte/products_list_admin.html', {
        'products': products,
    })

def contact_list_admin(request):
    contact = Contact.objects.all()

    return render(request, 'adminlte/contact_list_admin.html', {
        'contact': contact,
    }) 

def contact_details_admin(request, id):
    contact = get_object_or_404(Contact, id=id)
    return render(request, 'adminlte/contact_details_admin.html', {
        'contact': contact,
    })     