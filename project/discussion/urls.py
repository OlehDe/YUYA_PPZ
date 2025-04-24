from django.urls import path
from . import views
from .views import register_view, login_view, logout_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout', logout_view, name='logout'),

    path('', views.event_list, name='event_list'),  # Головна сторінка зі списком подій
    path('event/new/', views.event_create, name='event_create'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('event/<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('event/<int:pk>/delete/', views.event_delete, name='event_delete'),

    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),

    path('admin/users/', views.admin_user_list, name='admin_user_list'),
    path('admin/user/<int:pk>/change-password/', views.admin_change_password, name='admin_change_password'),
]
