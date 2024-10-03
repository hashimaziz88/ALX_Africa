# reviews/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Review, Comment, UserProfile

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['movie_title', 'review_content', 'rating', 'poster_url']
        widgets = {
            'movie_title': forms.TextInput(attrs={'readonly': 'readonly'}),  # Make it read-only to prevent manual editing
            'poster_url': forms.HiddenInput(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'favorite_genres']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
