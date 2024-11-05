# reviews/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Review, Comment, UserProfile

class ReviewForm(forms.ModelForm):
    """
    Form for creating and updating a review.
    """
    class Meta:
        model = Review
        fields = ['movie_title', 'review_content', 'rating', 'poster_url']
        widgets = {
            'movie_title': forms.TextInput(attrs={'readonly': 'readonly'}),
            'poster_url': forms.HiddenInput(),
        }

    def clean_rating(self):
        """
        Validate the rating field to ensure a rating is selected.
        """
        rating = self.cleaned_data.get('rating')
        if rating is None:
            raise forms.ValidationError('You must select a rating.')
        return rating


class CommentForm(forms.ModelForm):
    """
    Form for creating and updating comments.
    """
    class Meta:
        model = Comment
        fields = ['content']


class UserProfileForm(forms.ModelForm):
    """
    Form for creating and updating user profiles.
    """
    class Meta:
        model = UserProfile
        fields = ['bio', 'favorite_genres']


class CustomUserCreationForm(UserCreationForm):
    """
    Custom user creation form to include email field.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
