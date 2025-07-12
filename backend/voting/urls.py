
from django.urls import path
from . import views

# API Routes
api_patterns = [
    path('api/cast-vote/', views.cast_vote, name='cast-vote'),
    path('api/my-votes/', views.my_votes, name='my-votes'),
    path('api/results/<int:election_id>/', views.election_results, name='election-results'),
    path('api/sessions/', views.voting_sessions, name='voting-sessions'),
    path('api/eligibility/<int:election_id>/', views.check_voting_eligibility, name='voting-eligibility'),
]

# HTML Page Routes
page_patterns = [
    path('', views.vote_page, name='vote-page'),
    path('dashboard/', views.voter_dashboard_page, name='voter-dashboard'),
    path('guidline/', views.voter_guidline_page, name='voter-guidline'),
]

# Combine all patterns
urlpatterns = api_patterns + page_patterns
