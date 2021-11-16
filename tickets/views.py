from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Ticket, TicketComment
from .forms import TicketCreateForm, TicketCommentCreateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail

# Create your views here.
@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'tickets/ticket_list.html', {
        'tickets': tickets,
    })

@login_required
def ticket_details(request, id):
    ticket = get_object_or_404(Ticket, user_id=request.user.id, id=id)
    return render(request, 'tickets/ticket_details.html', {
        'ticket': ticket,
        'ticketcomment': TicketComment.objects.filter(ticket_id=id),
    })

@login_required
def add_ticket(request):
    if request.method == 'POST':
        form = TicketCreateForm(request.POST)
        if form.is_valid():
            ticket = Ticket()
            ticket.subject = form.cleaned_data['subject']
            ticket.text = form.cleaned_data['text']
            ticket.image = form.cleaned_data['image']
            ticket.user = request.user
            ticket.save()
            # تنظیمات ارسال فاکتور خرید با ایمیل
            subject = 'سوال شما ثبت شد'
            message = f'با سلام و خسته نباشید {request.user.username}'
            
            send_mail(subject,
            message,
            'coolgertn@gmail.com', 
            [ticket.user.email], 
            fail_silently=False)

            messages.success(request, 'تیکت شما با موفقیت ایجاد شد.')
            return HttpResponseRedirect(reverse('ticket:ticket_details', args=[ticket.id]))
    else:
        form = TicketCreateForm()
    return render(request, 'tickets/add_ticket.html', {
            'form': form,
        })

def add_ticketcomment(request, id):
    url = request.META.get('HTTP_REFERER')  
    if request.method == 'POST':
        form = TicketCommentCreateForm(request.POST)
        if form.is_valid():
            comment = TicketComment()
            comment.text = form.cleaned_data['text']
            comment.image = form.cleaned_data['image']
            comment.ticket_id = id
            comment.author_id = request.user.id 
            comment.save()
            # تنظیمات ارسال فاکتور خرید با ایمیل
            subject = 'سوال شما ثبت شد'
            message = f'با سلام و خسته نباشید {comment.ticket.user.username}'
            
            send_mail(subject,
            message,
            'coolgertn@gmail.com', 
            [comment.ticket.user.email], 
            fail_silently=False)

            messages.success(request, 'تیکت شما با موفقیت ثبت شد. ممنون از ارسال تیکت شما...')
            return HttpResponseRedirect(url)
    else:
        form = TicketCommentCreateForm()
    return HttpResponseRedirect(url)        