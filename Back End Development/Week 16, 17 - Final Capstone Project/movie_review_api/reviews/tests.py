from django.test import TestCase
from .forms import ReviewForm, CommentForm, UserProfileForm, CustomUserCreationForm
from .models import Review, Comment, UserProfile
from django.contrib.auth.models import User

class ReviewFormTest(TestCase):
    def test_review_form_valid(self):
        form_data = {
            'movie_title': 'Inception',
            'review_content': 'A mind-bending thriller.',
            'rating': 5,
            'poster_url': 'http://example.com/poster.jpg'
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_review_form_invalid_without_rating(self):
        form_data = {
            'movie_title': 'Inception',
            'review_content': 'A mind-bending thriller.',
            'rating': None,  # Invalid rating
            'poster_url': 'http://example.com/poster.jpg'
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

class CommentFormTest(TestCase):
    def test_comment_form_valid(self):
        form_data = {
            'content': 'Great movie!'
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_comment_form_invalid_without_content(self):
        form_data = {
            'content': ''  # Invalid content
        }
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)

class UserProfileFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user_profile = UserProfile.objects.create(user=self.user)

    def test_user_profile_form_valid(self):
        form_data = {
            'bio': 'I love movies!',
            'favorite_genres': 'Action, Drama'
        }
        form = UserProfileForm(data=form_data, instance=self.user_profile)
        self.assertTrue(form.is_valid())



class CustomUserCreationFormTest(TestCase):
    def test_user_creation_form_valid(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'Str0ng_P@ssw0rd!',  # Use a strong password
            'password2': 'Str0ng_P@ssw0rd!'
        }
        form = CustomUserCreationForm(data=form_data)
        if not form.is_valid():
            print(form.errors)  # Print errors for debugging
        self.assertTrue(form.is_valid())


