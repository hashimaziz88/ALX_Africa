from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class LibraryUser(AbstractUser):
    """
    User model extending AbstractUser.

    :param email: User's email address
    :param date_of_membership: The date the user became a member
    :param is_active: Whether the user is active
    """
    email = models.EmailField(unique=True)
    date_of_membership = models.DateField(auto_now_add=True)  # Add this field
    is_active = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        Group,
        related_name='library_users',  # Change this
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='library_users',  # Change this
        blank=True,
    )

class Book(models.Model):
    """
    Book model for storing book information.

    :param title: The title of the book
    :param author: The author of the book
    :param isbn: The unique ISBN number of the book
    :param published_date: The published date of the book
    :param available_copies: The number of available copies
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    available_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        """
        String representation of the Book model.
        :return: The title of the book
        """
        return self.title


class Transaction(models.Model):
    """
    Transaction model to track the checkout and return of books.

    :param user: The user who checked out the book
    :param book: The book being checked out or returned
    :param checkout_date: The date the book was checked out
    :param return_date: The date the book was returned
    """
    user = models.ForeignKey(LibraryUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    checkout_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        """
        String representation of the Transaction model.
        :return: User and book involved in the transaction
        """
        return f'{self.user} - {self.book}'
