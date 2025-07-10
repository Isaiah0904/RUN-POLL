
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Notification, SystemAnnouncement
from .serializers import NotificationSerializer, SystemAnnouncementSerializer

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def notifications_list(request):
    notifications = Notification.objects.filter(recipient=request.user)
    
    # Filter by read status if provided
    is_read = request.query_params.get('is_read')
    if is_read is not None:
        notifications = notifications.filter(is_read=is_read.lower() == 'true')
    
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def mark_notification_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.is_read = True
    notification.save()
    
    serializer = NotificationSerializer(notification)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def mark_all_read(request):
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return Response({'message': 'All notifications marked as read'})

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def unread_count(request):
    count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    return Response({'unread_count': count})

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def announcements_list(request):
    if request.method == 'GET':
        # Get active announcements for the user's type
        announcements = SystemAnnouncement.objects.filter(
            is_active=True,
            expires_at__gt=timezone.now()
        ).filter(
            models.Q(target_user_type='all') | 
            models.Q(target_user_type=request.user.user_type)
        )
        
        serializer = SystemAnnouncementSerializer(announcements, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        if request.user.user_type != 'admin':
            return Response({'error': 'Only administrators can create announcements'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        serializer = SystemAnnouncementSerializer(data=request.data)
        if serializer.is_valid():
            announcement = serializer.save(created_by=request.user)
            
            # Create notifications for target users
            create_announcement_notifications(announcement)
            
            return Response(SystemAnnouncementSerializer(announcement).data, 
                          status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def create_announcement_notifications(announcement):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Get target users
    if announcement.target_user_type == 'all':
        users = User.objects.filter(is_active=True)
    else:
        users = User.objects.filter(user_type=announcement.target_user_type, is_active=True)
    
    # Create notifications
    notifications = []
    for user in users:
        notifications.append(Notification(
            recipient=user,
            title=announcement.title,
            message=announcement.content,
            notification_type='system_announcement'
        ))
    
    Notification.objects.bulk_create(notifications)

# Utility functions for creating specific notifications
def create_notification(recipient, title, message, notification_type, action_url=None):
    """Helper function to create notifications"""
    Notification.objects.create(
        recipient=recipient,
        title=title,
        message=message,
        notification_type=notification_type,
        action_url=action_url
    )

def notify_election_created(election):
    """Notify users when a new election is created"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    voters = User.objects.filter(user_type='voter', is_active=True)
    for voter in voters:
        create_notification(
            recipient=voter,
            title=f"New Election: {election.title}",
            message=f"A new election '{election.title}' has been created. Registration is now open.",
            notification_type='election_created',
            action_url=f'/elections/{election.id}/'
        )

def notify_registration_status(registration, approved):
    """Notify voter about registration approval/rejection"""
    status_text = "approved" if approved else "rejected"
    title = f"Election Registration {status_text.title()}"
    message = f"Your registration for '{registration.election.title}' has been {status_text}."
    
    create_notification(
        recipient=registration.voter,
        title=title,
        message=message,
        notification_type=f'registration_{status_text}',
        action_url=f'/elections/{registration.election.id}/'
    )

def notify_vote_confirmation(vote):
    """Notify voter about successful vote"""
    create_notification(
        recipient=vote.voter,
        title="Vote Confirmed",
        message=f"Your vote for {vote.position.title} in '{vote.election.title}' has been recorded.",
        notification_type='vote_confirmation',
        action_url=f'/elections/{vote.election.id}/results/'
    )
