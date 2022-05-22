from django.shortcuts import render, get_object_or_404
from .models import Blog

# Create your views here.
def blog(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'blog/blog.html', {
        'blogs': blogs,
    })

def blog_details(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    return render(request, 'blog/blog_details.html', {
        'blog': blog,
    })    