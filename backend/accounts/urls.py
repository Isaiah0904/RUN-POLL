from django.urls import path
from . import views

urlpatterns = [
    # HTML Page Views
    path('', views.index_page, name='index'),
    path('login/', views.login_page, name='login_page'),
    path('register/', views.registration_page, name='registration_page'),
    path('forgot-password/', views.forgot_password_page, name='forgot_password_page'),
    path('reset-password/', views.reset_password_page, name='reset_password_page'),
    path('profile-settings/', views.profile_settings_page, name='profile_settings_page'),
    path('test-connection/', views.test_connection_page, name='test_connection_page'),
    
    # API Endpoints
    path('api/register/', views.register, name='register'),
    path('api/login/', views.login_view, name='login'),
    path('api/logout/', views.logout_view, name='logout'),
    path('api/profile/', views.profile_view, name='profile'),
    path('api/user-info/', views.user_info, name='user-info'),
]