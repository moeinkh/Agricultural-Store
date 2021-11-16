from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Order, OrderItem
from .forms import OrderForm
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils.crypto import get_random_string
from products.models import Product

from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from smtplib import SMTPAuthenticationError
from django.core.mail import send_mail
# Create your views here.
@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.user = request.user
            ordercode = get_random_string(8)
            order.order_code = ordercode
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                    total_price=item['total_price']
                )
                
                product = Product.objects.get(name=item['product'])
                product.count -= item['quantity']
                product.save()
            # clear the cart
            cart.clear()
            # clear the coupon code
            request.session['coupon_id'] = None
            # set order in session
            request.session['order_id'] = order.id   
            # تنظیمات ارسال فاکتور خرید با ایمیل
            subject = 'ثبت سفارش'
            message = f'با سلام و خسته نباشید {request.user.username}'
            send_mail(subject, message, 'coolgertn@gmail.com', [request.user.email], fail_silently=False)
            return redirect(reverse('product:home'))
    else:
        form = OrderForm()
    return render(request, 'orders/checkout.html', {
            'form': form,
            'cart': cart
        })        

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/admin_order_detail.html',
                  {'order': order})        