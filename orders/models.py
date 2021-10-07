from decimal import Decimal
from django.db import models
from accounts.models import User
from products.models import Product
from coupons.models import Coupon
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    first_name = models.CharField('نام', max_length=64)
    last_name = models.CharField('نام خانوادگی', max_length=64)
    city = models.CharField('شهر', max_length=128)
    address = models.CharField('آدرس', max_length=256)
    postal_code = models.CharField('کد پستی', max_length=16)
    phone_number = models.CharField('شماره تلفن', max_length=11)
    paid = models.BooleanField('پرداخت شد', default=False)
    order_code = models.CharField('کد سفارش', max_length=8)

    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, related_name='orders', null=True, blank=True, verbose_name='کد تخفیف')
    discount = models.IntegerField('تخفیف', default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروز رسانی', auto_now=True)

    

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'
        ordering = ('-created_at', )

    def __str__(self):
        return self.user.username

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal(100)) 

    get_total_cost.short_description = 'مبلغ کل'      


class OrderItem(models.Model):
    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='سفارش')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', verbose_name='محصول')
    price = models.PositiveIntegerField('قیمت')
    quantity = models.PositiveIntegerField('تعداد', default=1)

    def __str__(self):
        return self.product.name

    def get_cost(self):
        return self.quantity * self.price     

    get_cost.short_description = 'مبلغ' 