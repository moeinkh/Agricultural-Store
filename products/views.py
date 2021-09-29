from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Brand, Images, Comment
from .forms import CommentForm
from django.http import HttpResponseRedirect
from django.contrib import messages
# Create your views here.

def home(request):
    categories = Category.objects.all()
    product = Product.objects.filter(available=True)

    return render(request, 'products/home.html', {
        'product': product,
        'categories': categories,
        'last_product': Product.objects.all()[:3]
    })    

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    product = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        product = product.filter(category=category)

    return render(request, 'products/shop-grid.html', {
        'product': product,
        'categories': categories,
        'category': category,
        'last_product': Product.objects.all()[:3]
    })  

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    images = Images.objects.filter(product_id=id)

    return render(request, 'products/product-detail.html', {
        'product': product,
        'images': images,
        'related_product': Product.objects.filter(category=product.category).exclude(id=id)[:3],
        'comments': Comment.objects.filter(product_id=id, active=True).order_by('-created_at'),
        })

def add_comment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()
            data.comment = form.cleaned_data['comment']
            data.product_id = id
            data.user_id = request.user.id
            data.save()
            messages.success(request, 'نظر شما با موفقیت ثبت شد. ممنون از ارسال نظر شما...')
            return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)        