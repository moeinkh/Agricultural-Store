from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('order_list/', views.order_list, name='order_list'),
    path('order_list/<int:id>', views.order_details, name='order_details'),
]