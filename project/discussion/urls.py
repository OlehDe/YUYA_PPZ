from django.urls import path
from . import views
from .views import register_view, login_view

urlpatterns = [
    path('register', register_view, name='register'),
    path('login', login_view, name='login'),

    path('', views.base_event, name='base'),
    path('event/<int:event_id>/', views.event_details, name='event_details'),
    path('create_event/', views.create_event, name='create_event'),
]