from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer
from rest_framework import generics, permissions
from .serializers import UserProfileSerializer
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from rest_framework import viewsets


class UserViewSet(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        user = self.get_object()
        request.user.following.add(user)
        return Response({'status': 'following'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        user = self.get_object()
        request.user.following.remove(user)
        return Response({'status': 'unfollowed'}, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Returns the authenticated user's profile
        return self.request.user

    def get(self, request, *args, **kwargs):
        # Return user's profile information
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        # Update the authenticated user's profile
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)  # partial=True allows partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
