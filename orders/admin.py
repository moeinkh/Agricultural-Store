from django.contrib import admin
from .models import Order, OrderItem
from django.urls import reverse
from django.utils.safestring import mark_safe



# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['product', 'price', 'quantity', 'total_price']
    can_delete = False
    extra = 0
       

def order_detail(obj):
    url = reverse('order:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">جزئیات</a>')    

order_detail.short_description = 'جزئیات سفارش'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','city', 'address', 'postal_code', 'jcreated_at', 'paid', 'status','phone_number', 'get_total_cost', order_detail]
    list_filter = ['paid', 'created_at', 'updated_at']
    readonly_fields = ['order_code']
    search_fields = ['first_name', 'last_name', 'phone_number', 'order_code']
    inlines = [OrderItemInline]
    

