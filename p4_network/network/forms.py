from cProfile import label
from django import forms
from .models import *

class NewPostForm(forms.ModelForm):
    media = forms.ImageField(
        label='Upload media',
        widget=forms.ClearableFileInput(
            attrs={
                'multiple': True,
                'class': 'form-control'
            }
        ),
        required=False
    )
    
    class Meta:
        model = Post
        fields = [
            'media',
        ]