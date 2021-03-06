from django import forms
from .models import Comment,  Contact

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment', )

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'text')