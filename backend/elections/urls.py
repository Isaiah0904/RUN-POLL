from django.urls import path
from . import views

# API Routes
api_patterns = [
    path('api/', views.elections_list, name='elections-list'),
    path('api/<int:pk>/', views.election_detail, name='election-detail'),
    path('api/<int:pk>/candidates/', views.election_candidates, name='election-candidates'),
    path('api/candidates/', views.candidates_list, name='candidates-list'),
    path('api/candidates/<int:candidate_id>/', views.candidate_detail, name='candidate-detail'),
    path('api/register-candidate/', views.register_candidate, name='register-candidate'),
    path('api/dashboard-stats/', views.dashboard_stats, name='dashboard-stats'),
]

# HTML Page Routes
page_patterns = [
    path('', views.elections_dashboard_page, name='elections-dashboard'),
    path('election/<int:pk>/', views.election_detail_page, name='election-detail-page'),
    path('admin/dashboard/', views.elections_dashboard_page, name='admin-dashboard'),
    path('admin/election/', views.admin_election_page, name='admin-election'),
    path('admin/candidate/', views.admin_candidate_page, name='admin-candidate'),
    path('admin/voters/', views.admin_voters_page, name='admin-voters'),
    path('admin/results/', views.admin_results_page, name='admin-results'),
    path('admin/settings/', views.admin_settings_page, name='admin-settings'),
    path('admin/notification/', views.admin_notification_page, name='admin-notification'),
    path('candidate/', views.candidate_page, name='candidate-page'),
]

# Combine all patterns
urlpatterns = api_patterns + page_patterns