from django.contrib import admin
from .models import Ticket, TicketComment

# Register your models here.
class TicketCommentInliane(admin.TabularInline):
    model = TicketComment
    extra = 1


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'status', 'jcreated_at', 'jupdated_at']
    list_filter = ['user', 'subject', 'status', 'created_at']
    search_fields = ['uaer']
    inlines = [TicketCommentInliane]