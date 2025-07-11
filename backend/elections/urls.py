from django.urls import path
from . import views

urlpatterns = [
    path('', views.elections_list, name='elections-list'),
    path('<int:pk>/', views.election_detail, name='election-detail'),
    path('<int:pk>/candidates/', views.election_candidates, name='election-candidates'),
    path('candidates/', views.candidates_list, name='candidates-list'),
    path('candidates/<int:candidate_id>/', views.candidate_detail, name='candidate-detail'),
    path('register-candidate/', views.register_candidate, name='register-candidate'),
    path('dashboard-stats/', views.dashboard_stats, name='dashboard-stats'),
]