from django.urls import path
from . import views

app_name = 'ticket'

urlpatterns = [
    path('', views.ticket_list, name='ticket_list'),
    path('ticket_details/<int:id>/', views.ticket_details, name='ticket_details'),
    path('add_ticket/', views.add_ticket, name='add_ticket'),
    path('add_ticketcomment/<int:id>/', views.add_ticketcomment, name='add_ticketcomment'),
]