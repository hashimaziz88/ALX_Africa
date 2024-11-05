from django.contrib import admin
from .models import Review, Comment, UserProfile

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for the Review model.
    Displays movie title, user, rating, creation date, and poster URL.
    Allows searching by movie title and user, filtering by rating and creation date,
    and ordering by creation date (newest first).
    """
    list_display = ('movie_title', 'user', 'rating', 'created_date', 'poster_url')
    search_fields = ('movie_title', 'user__username')
    list_filter = ('rating', 'created_date')
    ordering = ('-created_date',)
    
    class CommentInline(admin.TabularInline):
        """
        Inline configuration for displaying Comment model within the Review admin panel.
        Displays user, content, and creation date, with read-only creation date.
        """
        model = Comment
        extra = 1
        fields = ('user', 'content', 'created_date')
        readonly_fields = ('created_date',)

    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for the Comment model.
    Displays review, user, content, and creation date.
    Allows searching by review movie title and user, and filtering by creation date.
    """
    list_display = ('review', 'user', 'content', 'created_date')
    search_fields = ('review__movie_title', 'user__username')
    list_filter = ('created_date',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for the UserProfile model.
    Displays user, bio, and favorite genres.
    Allows searching by username.
    """
    list_display = ('user', 'bio', 'favorite_genres')
    search_fields = ('user__username',)
