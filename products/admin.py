from django.contrib import admin
from .models import Category, Brand, Product

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']   

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'brand', 'country', 'weight', 'volume', 'count', 'price', 'available', 'image_tag']
    list_filter = ['name', 'country', 'created_at', 'available',]
    search_fields = ('name', 'country', 'brand', 'category')
    readonly_fields = ('image_tag',)