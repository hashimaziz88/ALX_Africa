# reviews/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Avg
from .models import Review, Comment, UserProfile
from .forms import ReviewForm, CommentForm, UserProfileForm, CustomUserCreationForm
import requests
from django.conf import settings
from django.shortcuts import render
import requests
from django.shortcuts import render
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import render
from django.db import models  # For Q objects
from .models import Review  # Assuming you have a Review model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserProfileForm
from .models import UserProfile



def review_list(request):
    movie_title = request.GET.get('movie_title', '')  
    search_query = request.GET.get('search', '')

    # Filter reviews by movie title and search query
    reviews = Review.objects.all()

    # If a movie title is provided, filter by it
    if movie_title:
        reviews = reviews.filter(movie_title__icontains=movie_title)

    # If a search query is provided, filter by both movie title and review content
    if search_query:
        reviews = reviews.filter(
            models.Q(movie_title__icontains=search_query) |  # Search in movie title
            models.Q(review_content__icontains=search_query)  # Search in review content
        )

    context = {
        'movie_title': movie_title,
        'reviews': reviews,
    }
    return render(request, 'review_list.html', context)


def search_movie(request):
    query = request.GET.get('title')
    movie_list = []
    
    if query:
        try:
            # Construct the OMDb API URL with the search query
            url = f"http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&s={query}"
            response = requests.get(url)
            
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                data = response.json()
                
                # Check if the API response contains a valid 'Search' result
                if 'Search' in data:
                    movie_list = data['Search']
                else:
                    # If there's no 'Search' result, display an appropriate message
                    messages.warning(request, "No movies found for your search query.")
            else:
                # Handle non-200 response codes from the OMDb API
                messages.error(request, "Failed to fetch data from OMDb. Please try again later.")
        except requests.exceptions.RequestException as e:
            # Handle network-related errors (e.g., connection issues)
            messages.error(request, f"An error occurred: {e}")
    
    return render(request, 'movie_search.html', {'movie_list': movie_list})

def home(request):
    latest_reviews = Review.objects.order_by('-created_date')[:5]
    return render(request, 'home.html', {'latest_reviews': latest_reviews})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user-profile')
    else:
        form = UserProfileForm(instance=profile)
    
    reviews = Review.objects.filter(user=request.user)
    return render(request, 'user_profile.html', {'form': form, 'reviews': reviews})

class ReviewListView(ListView):
    model = Review
    template_name = 'review_list.html'
    context_object_name = 'reviews'
    ordering = ['-created_date']
    paginate_by = 10

class ReviewDetailView(DetailView):
    model = Review
    template_name = 'review_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

from django.conf import settings
import requests
from django.urls import reverse_lazy

from django.contrib import messages
from django.shortcuts import redirect

from django.shortcuts import redirect
from django.contrib import messages
import requests
from django.conf import settings


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review_form.html'
    success_url = reverse_lazy('review-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie_title = self.request.GET.get('movie_title')

        if movie_title:
            url = f"http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t={movie_title}"
            response = requests.get(url)
            if response.status_code == 200:
                movie_details = response.json()
                context['movie_details'] = movie_details
                context['form'].initial['movie_title'] = movie_title
                context['form'].initial['poster_url'] = movie_details.get('Poster')
        
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.movie_title = self.request.GET.get('movie_title')

        movie_title = form.instance.movie_title
        if movie_title:
            url = f"http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t={movie_title}"
            response = requests.get(url)
            if response.status_code == 200:
                movie_details = response.json()
                form.instance.poster_url = movie_details.get('Poster')
        
        messages.success(self.request, 'Your review has been created successfully!')
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        movie_title = request.GET.get('movie_title')
        if not movie_title:
            messages.warning(request, 'Please search and select a movie before writing a review.')
            return redirect('search-movie')
        return super().get(request, *args, **kwargs)

class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review_form.html'
    success_url = reverse_lazy('review-list')

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user

    def form_valid(self, form):
        messages.success(self.request, 'Your review has been updated successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie_details'] = {
            'Title': self.object.movie_title,
            'Poster': self.object.poster_url,
            'Year': self.object.created_date.year  # You might want to store the movie year separately
        }
        return context

class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'reviews/review_confirm_delete.html'  # Ensures the correct template is used
    success_url = reverse_lazy('review-list')

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user


@login_required
def add_comment(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.review = review
            comment.user = request.user
            comment.save()
    return redirect('review-detail', pk=pk)

@login_required
def like_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user in review.likes.all():
        review.likes.remove(request.user)
    else:
        review.likes.add(request.user)
    return redirect('review-detail', pk=pk)

def get_movie_info(title):
    url = f"http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t={title}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

@login_required
def movie_recommendations(request):
    user_reviews = Review.objects.filter(user=request.user)
    favorite_genres = request.user.userprofile.favorite_genres.split(',')
    
    # Get highly rated movies from user's favorite genres
    recommended_movies = Review.objects.filter(
        rating__gte=4,
        movie_title__in=[review.movie_title for review in user_reviews]
    ).values('movie_title').annotate(avg_rating=Avg('rating')).order_by('-avg_rating')[:5]
    
    movies_with_info = []
    for movie in recommended_movies:
        movie_info = get_movie_info(movie['movie_title'])
        if movie_info:
            movies_with_info.append(movie_info)
    
    return render(request, 'movie_recommendations.html', {'recommended_movies': movies_with_info})

@login_required
def edit_user_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)  # Get the user's profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('user-profile')  # Redirect to the profile view
    else:
        form = UserProfileForm(instance=user_profile)
    
    context = {
        'form': form,
    }
    return render(request, 'edit_user_profile.html', context)