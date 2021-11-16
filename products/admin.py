from django.contrib import admin
from .models import (
    Category, 
    Brand, 
    Product, 
    Images, 
    Comment, 
    IpAddress, 
    ProductHit,
    Contact,
    Banner
    )
from mptt.admin import DraggableMPTTAdmin
from decimal import Decimal

# Register your models here.
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['name', 'parent']

admin.site.register(
    Category,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
        # ...more fields if you feel like it...
    ),
    list_display_links=(
        'indented_title',
    ),
)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']   

class ProductImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id', )
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'brand', 'country', 'weight', 'volume', 'count', 'price', 'discount', 'befor_discount', 'discount_status', 'available', 'image_tag']
    list_filter = ['category', 'brand', 'created_at', 'available',]
    search_fields = ('name', 'country', 'brand', 'category')
    readonly_fields = ('image_tag',)
    inlines = [ProductImageInline]
    actions = ['add_discount', 'remove_discount']


    # for add discount from products
    @admin.action(description='اعمال تخفیف')
    def add_discount(self, request, queryset):
        for q in queryset:
            if q.discount is not None:
                q.discount_status = True
                q.befor_discount = q.price
                q.price = q.price - ((q.discount / Decimal(100)) * q.price) 
                q.save(update_fields=['price', 'befor_discount', 'discount', 'discount_status'])


    # for remove discount from products
    @admin.action(description='حذف تخفیف')
    def remove_discount(self, request, queryset):
        for q in queryset:
            if q.discount is not None and q.befor_discount is None:
                q.discount = None
                q.save(update_fields=['discount'])
            elif q.discount is not None:
                q.discount_status = False
                q.price = q.befor_discount
                q.befor_discount = None
                q.discount = None
                q.save(update_fields=['price', 'befor_discount', 'discount', 'discount_status'])
         

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'active', 'jcreated_at'] 
    list_filter = ['active', 'created_at']
    search_fields = ('user', 'product')    

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'jcreated_at']
    search_fields = ('name', 'email')



admin.site.register(Banner)    
admin.site.register(IpAddress)    
admin.site.register(ProductHit)    