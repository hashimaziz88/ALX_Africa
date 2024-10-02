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
from .models import Review

def review_list(request):
    # Assuming you're retrieving the movie title somehow
    movie_title = request.GET.get('movie_title', '')  
    search_query = request.GET.get('search', '')

    # Filter reviews by movie title (or however you're determining which movie's reviews to show)
    reviews = Review.objects.filter(movie_title__icontains=movie_title)

    # Add search functionality if applicable
    if search_query:
        reviews = reviews.filter(review_content__icontains=search_query)

    context = {
        'movie_title': movie_title,
        'reviews': reviews,
    }
    return render(request, 'review_list.html', context)

def search_movie(request):
    if 'title' in request.GET:
        title = request.GET['title']
        url = f"http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&s={title}&r=json"
        response = requests.get(url)
        movies = response.json().get('Search', [])
    else:
        movies = []

    return render(request, 'movie_search.html', {'movies': movies})

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

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review_form.html'
    success_url = reverse_lazy('review-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get movie title from query params
        movie_title = self.request.GET.get('movie_title')

        # Fetch movie details from OMDb
        if movie_title:
            url = f"http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t={movie_title}"
            response = requests.get(url)
            if response.status_code == 200:
                context['movie_details'] = response.json()
                # Set the movie title in the form's initial data
                context['form'].initial['movie_title'] = movie_title
        
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.movie_title = self.request.GET.get('movie_title')  # Save the movie title from the query
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        # Ensure that movie title is provided, otherwise redirect to search
        movie_title = request.GET.get('movie_title')
        if not movie_title:
            return redirect('movie-search')  # Redirect to your search view
        return super().get(request, *args, **kwargs)

class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review_form.html'
    success_url = reverse_lazy('review-list')

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user

class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
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
