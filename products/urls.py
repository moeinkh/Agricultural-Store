from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.home, name = 'home'),
    path('contact/', views.contact, name = 'contact'),
    path('product_list', views.product_list, name = 'product_list'),
    path('product_list/<str:category_slug>/', views.product_list, name = 'product_list_category'),
    path('product_list_brand/<str:brand_slug>/', views.product_list, name = 'product_list_brand'),
    path('product_detail/<int:id>/<str:slug>/', views.product_detail, name='product_detail'),
    path('addـcomment/<int:id>/', views.add_comment, name='add_comment'),
]