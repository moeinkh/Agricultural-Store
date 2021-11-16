from django import forms
from .models import Ticket, TicketComment

class TicketCreateForm(forms.ModelForm):
    subject = forms.ChoiceField(choices=Ticket.SUBJECT_CHOICES)
    class Meta:
        model = Ticket
        fields = ('text', 'image')

class TicketCommentCreateForm(forms.ModelForm):
    class Meta:
        model = TicketComment
        fields = ('text', 'image')


class TicketCommentCreateAdminForm(forms.ModelForm):
    status = forms.ChoiceField(choices=Ticket.STATUS_CHOICES)
    class Meta:
        model = TicketComment
        fields = ('text', 'image')