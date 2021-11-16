from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.admin_panel, name='management'),
    path('ticket_details_admin/<int:id>/', views.ticket_details_admin_panel, name='ticket_details_admin'),
    path('add_ticketcomment_admin/<int:id>/', views.add_ticketcomment_admin, name='add_ticketcomment_admin'),
    path('orders_list_admin/', views.orders_list_admin, name='orders_list_admin'),
    path('tickets_list_admin/', views.tickets_list_admin, name='tickets_list_admin'),
    path('products_list_admin/', views.products_list_admin, name='products_list_admin'),
    path('contact_list_admin/', views.contact_list_admin, name='contact_list_admin'),
    path('contact_details_admin/<int:id>/', views.contact_details_admin, name='contact_details_admin'),
]