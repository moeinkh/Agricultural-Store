from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog, name='blog'),
    path('blog_details/<str:slug>', views.blog_details, name='blog_details'),
]