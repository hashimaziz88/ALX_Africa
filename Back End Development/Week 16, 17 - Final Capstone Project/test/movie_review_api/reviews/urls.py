from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('search/', views.search_movie, name='search-movie'),  # Endpoint for movie search
    path('reviews/', views.review_list, name='reviews-by-movie'),  # List reviews by movie
    path('register/', views.register, name='register'),  # User registration endpoint
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html', 
        redirect_authenticated_user=True, 
        next_page='user-profile'
    ), name='login'),  # User login endpoint
    path('logout/', auth_views.LogoutView.as_view(
        template_name='logout.html', 
        next_page='home'
    ), name='logout'),  # User logout endpoint
    path('user-profile/', views.user_profile, name='user-profile'),  # User profile view
    path('user-profile/edit/', views.edit_user_profile, name='profile-edit'),  # Edit user profile
    path('reviews/', views.ReviewListView.as_view(), name='review-list'),  # List all reviews
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),  # Review detail view
    path('reviews/new/', views.ReviewCreateView.as_view(), name='review-create'),  # Create new review
    path('reviews/<int:pk>/update/', views.ReviewUpdateView.as_view(), name='review-update'),  # Update review
    path('reviews/<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='review-delete'),  # Delete review
    path('reviews/<int:pk>/comment/', views.add_comment, name='add-comment'),  # Add comment to review
    path('reviews/<int:pk>/like/', views.like_review, name='like-review'),  # Like a review
    path('recommendations/', views.movie_recommendations, name='movie-recommendations'),  # Movie recommendations endpoint
]
