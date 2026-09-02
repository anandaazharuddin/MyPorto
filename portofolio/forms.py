from django import forms

from .models import Message


class ContactForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('name', 'email', 'subject', 'message')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
            'subject': forms.TextInput(attrs={'placeholder': 'What can I help with?'}),
            'message': forms.Textarea(attrs={'placeholder': 'Tell me about your project...', 'rows': 5}),
        }