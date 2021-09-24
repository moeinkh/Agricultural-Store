from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Brand
# Create your views here.
def home(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    product = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        product = product.filter(category=category)

    return render(request, 'products/home.html', {
        'product': product,
        'categories': categories,
        'category': category,
    })    