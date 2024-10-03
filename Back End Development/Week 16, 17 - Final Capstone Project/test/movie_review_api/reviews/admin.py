# admin.py

from django.contrib import admin
from .models import Review, Comment, UserProfile

# Admin for Review model
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie_title', 'user', 'rating', 'created_date', 'poster_url')  # Display relevant fields
    search_fields = ('movie_title', 'user__username')  # Enable search by movie title and username
    list_filter = ('rating', 'created_date')  # Enable filtering by rating and creation date
    ordering = ('-created_date',)  # Order reviews by creation date (newest first)
    
    # Optional: Add inline comments if you want to see comments in the Review admin page
    class CommentInline(admin.TabularInline):
        model = Comment
        extra = 1  # Number of empty forms to display
        fields = ('user', 'content', 'created_date')
        readonly_fields = ('created_date',)  # Make created date read-only

    inlines = [CommentInline]  # Display comments inline

# Admin for Comment model
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'user', 'content', 'created_date')  # Display relevant fields
    search_fields = ('review__movie_title', 'user__username')  # Enable search
    list_filter = ('created_date',)  # Enable filtering by creation date

# Admin for UserProfile model
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'favorite_genres')  # Display relevant fields
    search_fields = ('user__username',)  # Enable search by username

# You can register additional models similarly
