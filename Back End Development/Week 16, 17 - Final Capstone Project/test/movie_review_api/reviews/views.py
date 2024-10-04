from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Avg, Q
from django.core.paginator import Paginator
from django.contrib import messages
import random
import requests
from django.conf import settings

from .models import Review, Comment, UserProfile
from .forms import ReviewForm, CommentForm, UserProfileForm, CustomUserCreationForm

def review_list(request):
    """
    Display a list of reviews with optional filtering by movie title, search query, rating, and sorting. 
    Supports pagination.
    """
    movie_title = request.GET.get('movie_title', '')
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'created_date_desc')
    rating_filter = request.GET.get('rating', '')

    reviews = Review.objects.all()

    if movie_title:
        reviews = reviews.filter(movie_title__icontains=movie_title)

    if search_query:
        reviews = reviews.filter(
            Q(movie_title__icontains=search_query) | Q(review_content__icontains=search_query)
        )

    if rating_filter:
        rating_range = rating_filter.split('-')
        if len(rating_range) == 2:
            reviews = reviews.filter(rating__gte=rating_range[0], rating__lte=rating_range[1])

    if sort_by == 'rating':
        reviews = reviews.order_by('-rating')
    elif sort_by == 'created_date_asc':
        reviews = reviews.order_by('created_date')
    else:
        reviews = reviews.order_by('-created_date')

    paginator = Paginator(reviews, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'movie_title': movie_title,
        'search_query': search_query,
        'sort_by': sort_by,
        'rating_filter': rating_filter,
        'reviews': page_obj,
    }
    return render(request, 'review_list.html', context)

def search_movie(request):
    """
    Search for movies using the OMDb API. Supports sorting and pagination.
    """
    query = request.GET.get('title', '')
    sort_by = request.GET.get('sort', 'title')
    movie_list = []
    total_results = 0

    if query:
        try:
            url = f"http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&s={query}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if 'Search' in data:
                    movie_list = data['Search'][:30]
                    total_results = int(data.get('totalResults', 0))
                else:
                    messages.warning(request, "No movies found for your search query.")
            else:
                messages.error(request, "Failed to fetch data from OMDb. Please try again later.")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"An error occurred: {e}")

        if sort_by == 'title':
            movie_list = sorted(movie_list, key=lambda x: x['Title'])
        elif sort_by == 'year':
            movie_list = sorted(movie_list, key=lambda x: x['Year'])
        elif sort_by == 'reviews':
            movie_list = sorted(movie_list, key=lambda x: get_reviews_count(x['Title']), reverse=True)

    paginator = Paginator(movie_list, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    reviewed_movies = set(Review.objects.filter(user=request.user).values_list('movie_title', flat=True))

    context = {
        'movie_list': page_obj,
        'total_results': total_results,
        'query': query,
        'sort': sort_by,
        'reviewed_movies': reviewed_movies,
    }
    return render(request, 'movie_search.html', context)

def get_reviews_count(movie_title):
    """
    Stub function to return the number of reviews for a movie.
    """
    return 0

def home(request):
    """
    Display the homepage with the latest 6 reviews.
    """
    latest_reviews = Review.objects.order_by('-created_date')[:6]
    return render(request, 'home.html', {'latest_reviews': latest_reviews})

def register(request):
    """
    Handle user registration and profile creation.
    """
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
    """
    Display and allow updates to the user's profile. Supports pagination for user's reviews.
    """
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('user-profile')
    else:
        form = UserProfileForm(instance=profile)
    
    reviews_list = Review.objects.filter(user=request.user)
    paginator = Paginator(reviews_list, 6)
    page_number = request.GET.get('page', 1)
    reviews = paginator.get_page(page_number)

    return render(request, 'user_profile.html', {'form': form, 'reviews': reviews})

class ReviewListView(ListView):
    """
    View to display a list of reviews with pagination.
    """
    model = Review
    template_name = 'review_list.html'
    context_object_name = 'reviews'
    ordering = ['-created_date']
    paginate_by = 5

class ReviewDetailView(DetailView):
    """
    View to display the details of a single review and its associated comments.
    """
    model = Review
    template_name = 'review_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

class ReviewCreateView(LoginRequiredMixin, CreateView):
    """
    View to create a new review. Retrieves movie details from OMDb API.
    """
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
    """
    View to update an existing review. Only the author of the review can update it.
    """
    model = Review
    form_class = ReviewForm
    template_name = 'review_form.html'
    success_url = reverse_lazy('review-list')

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user

    def form_valid(self, form):
        if not form.instance.poster_url:
            form.instance.poster_url = self.get_object().poster_url
        messages.success(self.request, 'Your review has been updated successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie_details'] = {
            'Title': self.object.movie_title,
            'Poster': self.object.poster_url,
            'Year': self.object.created_date.year
        }
        return context


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View for deleting a review. Only the review's author can delete it.
    """
    model = Review
    template_name = 'reviews/review_confirm_delete.html'  # Ensures the correct template is used
    success_url = reverse_lazy('review-list')

    def test_func(self):
        """
        Check if the logged-in user is the author of the review.
        """
        review = self.get_object()
        return self.request.user == review.user

@login_required
def add_comment(request, pk):
    """
    View for adding a comment to a review.
    """
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
    """
    View for liking or unliking a review.
    """
    review = get_object_or_404(Review, pk=pk)
    if request.user in review.likes.all():
        review.likes.remove(request.user)
    else:
        review.likes.add(request.user)
    return redirect('review-detail', pk=pk)

def get_movie_info(title):
    """
    Fetch movie information from the OMDb API.
    """
    url = f"http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t={title}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

@login_required
def movie_recommendations(request):
    """
    Generate movie recommendations based on user's reviews and favorite genres.
    If no recommendations are found, provide random movie suggestions.
    """
    user_reviews = Review.objects.filter(user=request.user)
    favorite_genres = request.user.userprofile.favorite_genres.split(',')

    # Get highly rated movies from user's favorite genres
    recommended_movies = Review.objects.filter(
        rating__gte=4,
        movie_title__in=[review.movie_title for review in user_reviews]
    ).values('movie_title').annotate(avg_rating=Avg('rating')).order_by('-avg_rating')[:6]

    movies_with_info = []
    for movie in recommended_movies:
        movie_info = get_movie_info(movie['movie_title'])
        if movie_info:
            movies_with_info.append(movie_info)

    # If no recommendations, get random movies
    if not movies_with_info:
        movies_with_info = get_random_movies(3)

    return render(request, 'movie_recommendations.html', {'recommended_movies': movies_with_info})

def get_random_movies(count):
    """
    Fetch random movies from a predefined list.
    """
    movie_list = ['Inception', 'The Matrix', 'Interstellar', 'The Dark Knight', 'Pulp Fiction', 'Forrest Gump']
    random_movies = random.sample(movie_list, count)
    movies_with_info = []
    for movie_title in random_movies:
        movie_info = get_movie_info(movie_title)
        if movie_info:
            movies_with_info.append(movie_info)
    return movies_with_info

@login_required
def edit_user_profile(request):
    """
    View for editing the user's profile.
    """
    user_profile = get_object_or_404(UserProfile, user=request.user)  # Get the user's profile
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
