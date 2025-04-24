from django.contrib import admin
from .models import Event, Review, Comment


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'creator', 'created_at')
    list_filter = ('date', 'location', 'creator')
    search_fields = ('title', 'description', 'location')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('event', 'author', 'created_at')
    list_filter = ('event', 'author', 'created_at')
    search_fields = ('text', 'author__username', 'event__title')
