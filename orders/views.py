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

# Create your views here.
@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
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
                    quantity=item['quantity']
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
            messages.success(request, 'سفارش با موفقیت ثبت شد.')
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