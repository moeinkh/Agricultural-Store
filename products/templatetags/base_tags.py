from django import template
from ..models import Product
from django.db.models import Count


register = template.Library()


@register.inclusion_tag('tags/last_product.html')
def last_product(total=3):
    last_product = Product.objects.filter(available=True, discount_status=False)[:total]
    return {'last_product': last_product}

@register.inclusion_tag('tags/product_visited.html')
def product_visited(total=3):
    product_visited = Product.objects.filter(available=True, discount_status=False).annotate(
        num_hits=Count('hits')).order_by('-num_hits')[:total]
    return {'product_visited': product_visited}

@register.inclusion_tag('tags/discount_product.html')
def discount_product():
    discount_product = Product.objects.filter(discount_status=True)
    return {'discount_product': discount_product}    