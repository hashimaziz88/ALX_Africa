from django.urls import path
from . import views

"""
URL patterns for library system.

:param path: Defines the URL and corresponding view function
"""

urlpatterns = [

    path('books/', views.BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('users/', views.UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('checkout/', views.CheckoutBookView.as_view(), name='checkout-book'),
    path('return/', views.ReturnBookView.as_view(), name='return-book'),
    path('available-books/', views.AvailableBooksView.as_view(), name='available-books'),
]
