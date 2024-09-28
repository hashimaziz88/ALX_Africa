from django.urls import path
from .views import notifications_list, mark_as_read

urlpatterns = [
    path('', notifications_list, name='notifications-list'),
    path('<int:pk>/read/', mark_as_read, name='notification-read'),
]
