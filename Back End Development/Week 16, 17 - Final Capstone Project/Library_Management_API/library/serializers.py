from rest_framework import serializers
from .models import Book, User, Transaction


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    :param Meta: Defines fields to serialize
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.

    :param Meta: Defines fields to serialize
    """

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'published_date', 'available_copies']


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Transaction model.

    :param Meta: Defines fields to serialize
    """

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'book', 'checkout_date', 'return_date']
