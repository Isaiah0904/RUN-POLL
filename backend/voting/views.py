
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from .models import Vote, VotingSession
from .serializers import VoteSerializer, CastVoteSerializer, VotingSessionSerializer
from elections.models import Election, Position, Candidate, ElectionRegistration

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def cast_vote(request):
    if request.user.user_type != 'voter':
        return Response({'error': 'Only voters can cast votes'}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    serializer = CastVoteSerializer(data=request.data)
    if serializer.is_valid():
        election = serializer.validated_data['election']
        votes_data = serializer.validated_data['votes']
        
        # Check if voter is registered for this election
        try:
            registration = ElectionRegistration.objects.get(
                voter=request.user, 
                election=election,
                status='approved'
            )
        except ElectionRegistration.DoesNotExist:
            return Response({'error': 'You are not registered for this election'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        # Check if voter has already voted in this election
        if Vote.objects.filter(voter=request.user, election=election).exists():
            return Response({'error': 'You have already voted in this election'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Start voting session
        voting_session = VotingSession.objects.create(
            voter=request.user,
            election=election,
            ip_address=get_client_ip(request)
        )
        
        try:
            with transaction.atomic():
                created_votes = []
                
                for vote_data in votes_data:
                    position = Position.objects.get(
                        id=vote_data['position_id'], 
                        election=election
                    )
                    candidate = Candidate.objects.get(
                        id=vote_data['candidate_id'],
                        position=position,
                        is_approved=True
                    )
                    
                    vote = Vote.objects.create(
                        voter=request.user,
                        candidate=candidate,
                        position=position,
                        election=election
                    )
                    created_votes.append(vote)
                
                # Complete voting session
                voting_session.end_time = timezone.now()
                voting_session.is_completed = True
                voting_session.save()
                
                # Serialize the created votes
                vote_serializer = VoteSerializer(created_votes, many=True)
                
                return Response({
                    'message': 'Votes cast successfully',
                    'votes': vote_serializer.data,
                    'session_id': voting_session.id
                }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response({'error': f'Error casting votes: {str(e)}'}, 
                          status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_votes(request):
    if request.user.user_type != 'voter':
        return Response({'error': 'Only voters can view their votes'}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    votes = Vote.objects.filter(voter=request.user)
    
    election_id = request.query_params.get('election')
    if election_id:
        votes = votes.filter(election_id=election_id)
    
    serializer = VoteSerializer(votes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def election_results(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    
    # Check if user can view results
    if election.results_visibility == 'private' and request.user.user_type != 'admin':
        return Response({'error': 'Results are not public'}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    if election.results_visibility == 'public' and election.status != 'completed':
        return Response({'error': 'Results will be available after election ends'}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    results = []
    for position in election.positions.all():
        candidates_results = []
        total_position_votes = position.total_votes
        
        for candidate in position.candidates.filter(is_approved=True):
            vote_count = candidate.vote_count
            percentage = (vote_count / total_position_votes * 100) if total_position_votes > 0 else 0
            
            candidates_results.append({
                'candidate_id': candidate.id,
                'candidate_name': f"{candidate.user.voter_profile.first_name} {candidate.user.voter_profile.last_name}",
                'vote_count': vote_count,
                'percentage': round(percentage, 2),
                'department': candidate.user.voter_profile.department,
            })
        
        # Sort candidates by vote count (descending)
        candidates_results.sort(key=lambda x: x['vote_count'], reverse=True)
        
        results.append({
            'position_id': position.id,
            'position_title': position.title,
            'total_votes': total_position_votes,
            'candidates': candidates_results
        })
    
    return Response({
        'election_id': election.id,
        'election_title': election.title,
        'status': election.status,
        'total_votes': election.total_votes,
        'results': results
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def voting_sessions(request):
    if request.user.user_type == 'admin':
        sessions = VotingSession.objects.all()
    else:
        sessions = VotingSession.objects.filter(voter=request.user)
    
    serializer = VotingSessionSerializer(sessions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def check_voting_eligibility(request, election_id):
    if request.user.user_type != 'voter':
        return Response({'eligible': False, 'reason': 'Only voters can participate'})
    
    election = get_object_or_404(Election, id=election_id)
    
    # Check if election is active
    if not election.is_active:
        return Response({'eligible': False, 'reason': 'Election is not currently active'})
    
    # Check if voter is registered
    try:
        registration = ElectionRegistration.objects.get(
            voter=request.user,
            election=election
        )
        if registration.status != 'approved':
            return Response({
                'eligible': False, 
                'reason': f'Registration is {registration.status}'
            })
    except ElectionRegistration.DoesNotExist:
        return Response({'eligible': False, 'reason': 'Not registered for this election'})
    
    # Check if already voted
    if Vote.objects.filter(voter=request.user, election=election).exists():
        return Response({'eligible': False, 'reason': 'Already voted in this election'})
    
    return Response({'eligible': True, 'reason': 'Eligible to vote'})
