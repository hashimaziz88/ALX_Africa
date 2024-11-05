from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    """
    Model representing a movie review.
    Attributes:
        movie_title: The title of the movie being reviewed.
        review_content: The content of the review.
        rating: The rating given to the movie (1 to 5).
        user: The user who created the review.
        created_date: The date when the review was created.
        likes: Users who liked the review.
        poster_url: URL of the movie poster.
    """
    movie_title = models.CharField(max_length=255)
    review_content = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_reviews', blank=True)
    poster_url = models.URLField(max_length=500, blank=True, null=True)  # URL of the movie poster

    def __str__(self):
        return f"{self.movie_title} - {self.user.username}"

class Comment(models.Model):
    """
    Model representing a comment on a review.
    Attributes:
        review: The review to which this comment belongs.
        user: The user who made the comment.
        content: The content of the comment.
        created_date: The date when the comment was created.
    """
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.review.movie_title}"

class UserProfile(models.Model):
    """
    Model representing a user's profile.
    Attributes:
        user: The user associated with this profile.
        bio: A brief biography of the user.
        favorite_genres: The user's favorite movie genres.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    favorite_genres = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username

