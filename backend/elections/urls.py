
from django.urls import path
from . import views

urlpatterns = [
    path('', views.elections_list, name='elections-list'),
    path('<int:pk>/', views.election_detail, name='election-detail'),
    path('<int:pk>/candidates/', views.election_candidates, name='election-candidates'),
    path('register-candidate/', views.register_candidate, name='register-candidate'),
    path('registrations/', views.election_registrations, name='election-registrations'),
    path('registrations/<int:pk>/approve/', views.approve_registration, name='approve-registration'),
    path('dashboard-stats/', views.dashboard_stats, name='dashboard-stats'),
]
