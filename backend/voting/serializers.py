
from rest_framework import serializers
from .models import Vote, VotingSession
from elections.models import Candidate, Position, Election

class VoteSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(source='candidate.user.voter_profile.first_name', read_only=True)
    position_title = serializers.CharField(source='position.title', read_only=True)
    
    class Meta:
        model = Vote
        fields = ['id', 'candidate', 'position', 'election', 'timestamp', 
                 'candidate_name', 'position_title']
        read_only_fields = ['timestamp']

class CastVoteSerializer(serializers.Serializer):
    election_id = serializers.IntegerField()
    votes = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField()
        )
    )
    
    def validate(self, attrs):
        election_id = attrs['election_id']
        votes_data = attrs['votes']
        
        try:
            election = Election.objects.get(id=election_id)
        except Election.DoesNotExist:
            raise serializers.ValidationError("Election does not exist")
        
        if not election.is_active:
            raise serializers.ValidationError("Election is not currently active")
        
        # Validate each vote
        for vote_data in votes_data:
            position_id = vote_data.get('position_id')
            candidate_id = vote_data.get('candidate_id')
            
            try:
                position = Position.objects.get(id=position_id, election=election)
                candidate = Candidate.objects.get(
                    id=candidate_id, 
                    position=position, 
                    is_approved=True
                )
            except (Position.DoesNotExist, Candidate.DoesNotExist):
                raise serializers.ValidationError("Invalid position or candidate")
        
        attrs['election'] = election
        return attrs

class VotingSessionSerializer(serializers.ModelSerializer):
    election_title = serializers.CharField(source='election.title', read_only=True)
    
    class Meta:
        model = VotingSession
        fields = ['id', 'election', 'start_time', 'end_time', 'is_completed', 
                 'election_title']
        read_only_fields = ['start_time', 'end_time']
