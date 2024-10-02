from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Book, User, Transaction
from .serializers import BookSerializer, UserSerializer, TransactionSerializer
from rest_framework.permissions import AllowAny


class BookListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating books.

    :param request: HTTP request object
    :param args: Additional arguments
    :param kwargs: Additional keyword arguments
    :return: Serialized list of books or created book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting a book.

    :param request: HTTP request object
    :param args: Additional arguments
    :param kwargs: Additional keyword arguments
    :return: Serialized book data or confirmation of update/deletion
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class UserListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating users.

    :param request: HTTP request object
    :param args: Additional arguments
    :param kwargs: Additional keyword arguments
    :return: Serialized list of users or created user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting a user.

    :param request: HTTP request object
    :param args: Additional arguments
    :param kwargs: Additional keyword arguments
    :return: Serialized user data or confirmation of update/deletion
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


def post(request, *args, **kwargs):
    """
    Handles the checkout of a book by a user.

    :param request: HTTP request object containing user and book info
    :param args: Additional arguments
    :param kwargs: Additional keyword arguments
    :return: Serialized transaction or error message
    """
    user = request.user
    book_id = request.data.get('book_id')
    book = Book.objects.get(id=book_id)

    if book.available_copies < 1:
        return Response({"error": "No copies available"}, status=status.HTTP_400_BAD_REQUEST)

    transaction = Transaction.objects.create(user=user, book=book)
    book.available_copies -= 1
    book.save()

    return Response(TransactionSerializer(transaction).data)


class CheckoutBookView(generics.GenericAPIView):
    """
    API view to handle book checkout by users.

    :param request: HTTP request object containing user and book info
    :param args: Additional arguments
    :param kwargs: Additional keyword arguments
    :return: Serialized transaction data or error message if book is unavailable
    """
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]


class ReturnBookView(generics.GenericAPIView):
    """
    API view to handle book return by users.

    :param request: HTTP request object containing user and book info
    :param args: Additional arguments
    :param kwargs: Additional keyword arguments
    :return: Serialized transaction data or error message if transaction not found
    """
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Handles the return of a checked-out book by a user.

        :param request: HTTP request object containing user and book info
        :param args: Additional arguments
        :param kwargs: Additional keyword arguments
        :return: Serialized transaction or error message
        """
        user = request.user
        book_id = request.data.get('book_id')
        book = Book.objects.get(id=book_id)
        transaction = Transaction.objects.filter(user=user, book=book, return_date__isnull=True).first()

        if not transaction:
            return Response({"error": "No active transaction for this book"}, status=status.HTTP_400_BAD_REQUEST)

        transaction.return_date = timezone.now()
        transaction.save()
        book.available_copies += 1
        book.save()

        return Response(TransactionSerializer(transaction).data)


class AvailableBooksView(generics.ListAPIView):
    """
    API view for listing available books.

    :param request: HTTP request object
    :param args: Additional arguments
    :param kwargs: Additional keyword arguments
    :return: Serialized list of available books
    """
    serializer_class = BookSerializer

    def get_queryset(self):
        """
        Retrieves the queryset of available books.

        :param request: HTTP request object
        :param args: Additional arguments
        :param kwargs: Additional keyword arguments
        :return: Queryset of books with available copies greater than zero
        """
        return Book.objects.filter(available_copies__gt=0)
