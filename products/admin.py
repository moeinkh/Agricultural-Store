from django.contrib import admin
from .models import Category, Brand, Product, Images, Comment
from mptt.admin import DraggableMPTTAdmin

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
    list_display = ['name', 'category', 'brand', 'country', 'weight', 'volume', 'count', 'price', 'available', 'image_tag']
    list_filter = ['name', 'country', 'created_at', 'available',]
    search_fields = ('name', 'country', 'brand', 'category')
    readonly_fields = ('image_tag',)
    inlines = [ProductImageInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'active'] 
    list_filter = ['active', 'created_at']
    search_fields = ('user', 'product')    