
from django.urls import path
from . import views

# API Routes
api_patterns = [
    path('api/', views.notifications_list, name='notifications-list'),
    path('api/<int:pk>/read/', views.mark_notification_read, name='mark-notification-read'),
    path('api/mark-all-read/', views.mark_all_read, name='mark-all-read'),
    path('api/unread-count/', views.unread_count, name='unread-count'),
    path('api/announcements/', views.announcements_list, name='announcements-list'),
]

# HTML Page Routes
page_patterns = [
    path('', views.notifications_page, name='notifications-page'),
]

# Combine all patterns
urlpatterns = api_patterns + page_patterns
