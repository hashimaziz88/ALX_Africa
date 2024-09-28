from django.urls import path, include

from . import views
from .views import RegisterView, LoginView, UserProfileView
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('', include(router.urls)),
    path('unfollow/<int:user_id>/', views.unfollow, name='unfollow'),
    path('follow/<int:user_id>', views.follow, name='follow'),
]
