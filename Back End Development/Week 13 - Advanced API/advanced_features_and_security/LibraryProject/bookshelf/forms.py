# LibraryProject/bookshelf/forms.py

from django import forms

class ExampleForm(forms.Form):
    title = forms.CharField(max_length=100, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
