from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Brand, Images, Comment, IpAddress
from .forms import CommentForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from cart.forms import CartAddProductForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.core.paginator import Paginator
# Create your views here.

def home(request):
    categories = Category.objects.all()
    product = Product.objects.filter(available=True)
    product_visited = Product.objects.filter(available=True).annotate(
        num_hits=Count('hits')).order_by('-num_hits')[:3]

    return render(request, 'products/home.html', {
        'product': product,
        'categories': categories,
        'last_product': Product.objects.all()[:3],
        'product_visited': product_visited,
    })    

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    product = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        product = product.filter(category=category)

    search_name = request.GET.get('search')
    if search_name:
        product = Product.objects.filter(Q(name__icontains=search_name)
                                        | Q(category__name__in=request.GET.getlist('search')))    

    paginator = Paginator(product, 15)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = paginator.page(p.num_pages)
    
    return render(request, 'products/shop-grid.html', {
        'product': product,
        'categories': categories,
        'category': category,
        'last_product': Product.objects.all()[:3],
        'page_obj': page_obj,
    })  

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    images = Images.objects.filter(product_id=id)
    cart_product_form = CartAddProductForm()

    # for visit
    for ip_address in IpAddress.objects.all():
        if ip_address not in product.hits.all():
            product.hits.add(ip_address)

    return render(request, 'products/product-detail.html', {
        'product': product,
        'images': images,
        'cart_product_form': cart_product_form,
        'related_product': Product.objects.filter(category=product.category).exclude(id=id)[:3],
        'comments': Comment.objects.filter(product_id=id, active=True).order_by('-created_at'),
        })

@login_required
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

def contact(request):

    return render(request, 'products/contact.html')    