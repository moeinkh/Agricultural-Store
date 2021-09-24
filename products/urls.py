from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.home, name = 'home'),
    path('<slug:category_slug>/', views.home, name = 'home_category'),
]