
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Election, Position, Candidate, ElectionRegistration
from .serializers import (
    ElectionSerializer, ElectionCreateSerializer, CandidateSerializer,
    CandidateRegistrationSerializer, ElectionRegistrationSerializer
)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def elections_list(request):
    if request.method == 'GET':
        elections = Election.objects.all()
        
        # Filter by status if provided
        status_filter = request.query_params.get('status')
        if status_filter:
            elections = elections.filter(status=status_filter)
        
        # Update election statuses
        for election in elections:
            election.update_status()
        
        paginator = StandardResultsSetPagination()
        result_page = paginator.paginate_queryset(elections, request)
        serializer = ElectionSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    elif request.method == 'POST':
        # Only admins can create elections
        if request.user.user_type != 'admin':
            return Response({'error': 'Only administrators can create elections'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        serializer = ElectionCreateSerializer(data=request.data)
        if serializer.is_valid():
            election = serializer.save(created_by=request.user)
            return Response(ElectionSerializer(election).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ...existing code...

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def candidates_list(request):
    """
    Returns a list of all approved candidates.
    """
    candidates = Candidate.objects.filter(is_approved=True)
    serializer = CandidateSerializer(candidates, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def candidate_detail(request, candidate_id):
    """
    Retrieve details of a specific candidate by ID.
    """
    candidate = get_object_or_404(Candidate, id=candidate_id)
    serializer = CandidateSerializer(candidate)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def election_detail(request, pk):
    election = get_object_or_404(Election, pk=pk)
    
    if request.method == 'GET':
        election.update_status()
        serializer = ElectionSerializer(election)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        if request.user.user_type != 'admin':
            return Response({'error': 'Only administrators can update elections'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        serializer = ElectionCreateSerializer(election, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(ElectionSerializer(election).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        if request.user.user_type != 'admin':
            return Response({'error': 'Only administrators can delete elections'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        election.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def election_candidates(request, pk):
    election = get_object_or_404(Election, pk=pk)
    
    position_id = request.query_params.get('position')
    if position_id:
        candidates = Candidate.objects.filter(
            position__election=election, 
            position_id=position_id,
            is_approved=True
        )
    else:
        candidates = Candidate.objects.filter(
            position__election=election,
            is_approved=True
        )
    
    serializer = CandidateSerializer(candidates, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def register_candidate(request):
    if request.user.user_type != 'voter':
        return Response({'error': 'Only voters can register as candidates'}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    serializer = CandidateRegistrationSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        candidate = serializer.save()
        return Response(CandidateSerializer(candidate).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def election_registrations(request):
    if request.method == 'GET':
        if request.user.user_type == 'admin':
            registrations = ElectionRegistration.objects.all()
        else:
            registrations = ElectionRegistration.objects.filter(voter=request.user)
        
        serializer = ElectionRegistrationSerializer(registrations, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        if request.user.user_type != 'voter':
            return Response({'error': 'Only voters can register for elections'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        serializer = ElectionRegistrationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            registration = serializer.save()
            return Response(ElectionRegistrationSerializer(registration).data, 
                          status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def approve_registration(request, pk):
    if request.user.user_type != 'admin':
        return Response({'error': 'Only administrators can approve registrations'}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    registration = get_object_or_404(ElectionRegistration, pk=pk)
    action = request.data.get('action')  # 'approve' or 'reject'
    
    if action == 'approve':
        registration.status = 'approved'
    elif action == 'reject':
        registration.status = 'rejected'
    else:
        return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
    
    registration.approved_by = request.user
    registration.save()
    
    return Response(ElectionRegistrationSerializer(registration).data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_stats(request):
    if request.user.user_type == 'admin':
        active_elections = Election.objects.filter(status='ongoing').count()
        total_elections = Election.objects.count()
        total_candidates = Candidate.objects.filter(is_approved=True).count()
        pending_registrations = ElectionRegistration.objects.filter(status='pending').count()
        
        return Response({
            'active_elections': active_elections,
            'total_elections': total_elections,
            'total_candidates': total_candidates,
            'pending_registrations': pending_registrations,
        })
    
    elif request.user.user_type == 'voter':
        available_elections = Election.objects.filter(status='ongoing').count()
        my_registrations = ElectionRegistration.objects.filter(voter=request.user).count()
        approved_registrations = ElectionRegistration.objects.filter(
            voter=request.user, status='approved'
        ).count()
        
        return Response({
            'available_elections': available_elections,
            'my_registrations': my_registrations,
            'approved_registrations': approved_registrations,
        })
    
    return Response({'error': 'Invalid user type'}, status=status.HTTP_400_BAD_REQUEST)
