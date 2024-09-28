from rest_framework import viewsets, permissions, generics
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Post, Like
from notifications.models import Notification


@api_view(['POST'])
def like_post(request, pk):
    post = generics.get_object_or_404(Post, pk=pk)  # Use get_object_or_404 for retrieving the post
    like, created = Like.objects.get_or_create(user=request.user, post=post)  # Create or get the existing like

    if not created:
        return JsonResponse({'message': 'You have already liked this post.'})

    # Generate notification if like is created
    Notification.objects.create(
        recipient=post.author,
        actor=request.user,
        verb='liked',
        target=post
    )

    return JsonResponse({'message': 'Post liked successfully.'})


@api_view(['POST'])
def unlike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)  # Use get_object_or_404 for retrieving the post
    like = Like.objects.filter(user=request.user, post=post).first()

    if not like:
        return JsonResponse({'message': 'You haven’t liked this post yet.'})

    like.delete()  # Delete the like

    return JsonResponse({'message': 'Post unliked successfully.'})


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(author__in=following_users).order_by
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['title', 'content']
    search_fields = ['title', 'content']

    @action(detail=False, methods=['get'])
    def feed(self, request):
        user = request.user
        posts = Post.objects.filter(author__in=user.following.all()).order_by('-created_at')
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
