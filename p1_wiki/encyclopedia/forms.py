from django import forms

class NewSearchFrom(forms.Form):
    query = forms.CharField(
        label='', 
        widget=forms.TextInput(attrs={
            'placeholder': 'Search encyclopedia',
            'class': 'search'
        })
    )
    
class NewEntryForm(forms.Form):
    title = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': "Entry title",
            'class': "entrytitle"
        })
    )
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'placeholder': "Entry content",
        })
    )

class NewEditForm(forms.Form):
    editedContent = forms.CharField(
        label='',
        initial="Something for now",
        widget=forms.Textarea(attrs={
            'placeholder': "Entry content"
        },)
    )
    
