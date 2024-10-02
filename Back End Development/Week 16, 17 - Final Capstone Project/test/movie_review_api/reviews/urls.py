from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import search_movie, review_list
from .views import ReviewCreateView


urlpatterns = [
    path('', views.home, name='home'),
    path('search/', search_movie, name='search-movie'),
    path('reviews/', review_list, name='reviews-by-movie'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True, next_page='user-profile'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html', next_page='home'), name='logout'),
    path('user-profile/', views.user_profile, name='user-profile'),
    path('reviews/', views.ReviewListView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
    path('reviews/new/', views.ReviewCreateView.as_view(), name='review-create'),
    path('reviews/<int:pk>/update/', views.ReviewUpdateView.as_view(), name='review-update'),
    path('reviews/<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='review-delete'),
    path('reviews/<int:pk>/comment/', views.add_comment, name='add-comment'),
    path('reviews/<int:pk>/like/', views.like_review, name='like-review'),
    path('recommendations/', views.movie_recommendations, name='movie-recommendations'),
    path('review/new/', ReviewCreateView.as_view(), name='review-create'),

]
