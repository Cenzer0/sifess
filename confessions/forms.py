from django import forms
from .models import Confession

class ConfessionForm(forms.ModelForm):
    class Meta:
        model = Confession
        fields = ['content_encrypted', 'mood'] # Image is optional and separate for now
        widgets = {
            'content_encrypted': forms.Textarea(attrs={
                'class': 'w-full p-4 border-2 border-gray-800 rounded-lg shadow-cartoon focus:outline-none focus:border-sifess-pink resize-none',
                'placeholder': 'Send me an anonymous message...',
                'rows': 4
            }),
            'mood': forms.HiddenInput()
        }
