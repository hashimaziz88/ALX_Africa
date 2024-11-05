from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Review, Comment, UserProfile

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    
    Attributes:
        password: The password for the user, write-only.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        """
        Create a new user with the validated data.
        
        Args:
            validated_data: The validated data for creating a user.
        
        Returns:
            User instance created with the validated data.
        """
        user = User.objects.create_user(**validated_data)
        return user

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.
    
    Attributes:
        user: The username of the user who made the comment, read-only.
    """
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_date']

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.
    
    Attributes:
        user: The username of the user who made the review, read-only.
        comments: List of comments associated with the review.
        likes_count: Count of likes for the review.
    """
    user = serializers.ReadOnlyField(source='user.username')
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'movie_title', 'review_content', 'rating', 'user', 'created_date', 'comments', 'likes_count']

    def get_likes_count(self, obj):
        """
        Retrieve the count of likes for the review.
        
        Args:
            obj: The Review instance.
        
        Returns:
            The number of likes for the review.
        """
        return obj.likes.count()

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserProfile model.
    
    Attributes:
        user: The user associated with this profile, read-only.
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'bio', 'favorite_genres']

