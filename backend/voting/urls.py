
from django.urls import path
from . import views

urlpatterns = [
    path('cast-vote/', views.cast_vote, name='cast-vote'),
    path('my-votes/', views.my_votes, name='my-votes'),
    path('results/<int:election_id>/', views.election_results, name='election-results'),
    path('sessions/', views.voting_sessions, name='voting-sessions'),
    path('eligibility/<int:election_id>/', views.check_voting_eligibility, name='voting-eligibility'),
]
