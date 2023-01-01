from .models import Auction, Bid, Comment
from django import forms

class NewAuctionForm(forms.ModelForm):    
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = Auction
        fields = [
            'title',
            'price',
            'description',
            'details',
            'category',
            'condition',
            'images',
        ]

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        labels = {
            'comment': ''
        }
        widgets = {
            'comment': forms.Textarea(attrs={
                'label': '',
                'class': "form-control",
                'placeholder': 'Comment something here.',
                'rows': 2
            })
        }
        fields = [
            'comment'
        ]
        
class NewBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = [
            'bid_amount'
        ]