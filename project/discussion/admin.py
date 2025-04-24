from django.contrib import admin
from .models import Event, Review

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'organizer')
    list_filter = ('date', 'location')
    search_fields = ('title', 'description')
    date_hierarchy = 'date'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'timestamp')
    list_filter = ('event', 'user')
    search_fields = ('content', )