
from rest_framework import serializers
from .models import Election, Position, Candidate, ElectionRegistration
from accounts.serializers import VoterProfileSerializer

class PositionSerializer(serializers.ModelSerializer):
    total_votes = serializers.ReadOnlyField()
    
    class Meta:
        model = Position
        fields = ['id', 'title', 'description', 'max_candidates', 'total_votes']

class CandidateSerializer(serializers.ModelSerializer):
    vote_count = serializers.ReadOnlyField()
    vote_percentage = serializers.ReadOnlyField()
    candidate_name = serializers.CharField(source='user.voter_profile.first_name', read_only=True)
    candidate_last_name = serializers.CharField(source='user.voter_profile.last_name', read_only=True)
    student_id = serializers.CharField(source='user.voter_profile.student_id', read_only=True)
    department = serializers.CharField(source='user.voter_profile.department', read_only=True)
    
    class Meta:
        model = Candidate
        fields = ['id', 'manifesto', 'profile_image', 'is_approved', 
                 'registration_date', 'vote_count', 'vote_percentage',
                 'candidate_name', 'candidate_last_name', 'student_id', 'department']

class ElectionSerializer(serializers.ModelSerializer):
    positions = PositionSerializer(many=True, read_only=True)
    total_votes = serializers.ReadOnlyField()
    is_active = serializers.ReadOnlyField()
    created_by_name = serializers.CharField(source='created_by.admin_profile.first_name', read_only=True)
    
    class Meta:
        model = Election
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 
                 'status', 'results_visibility', 'eligible_departments',
                 'positions', 'total_votes', 'is_active', 'created_by_name',
                 'created_at', 'updated_at']

class ElectionCreateSerializer(serializers.ModelSerializer):
    positions = serializers.ListField(
        child=serializers.DictField(), write_only=True, required=False
    )
    
    class Meta:
        model = Election
        fields = ['title', 'description', 'start_date', 'end_date',
                 'results_visibility', 'eligible_departments', 'positions']
    
    def create(self, validated_data):
        positions_data = validated_data.pop('positions', [])
        election = Election.objects.create(**validated_data)
        
        for position_data in positions_data:
            Position.objects.create(election=election, **position_data)
        
        return election

class CandidateRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['position', 'manifesto', 'profile_image']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ElectionRegistrationSerializer(serializers.ModelSerializer):
    election_title = serializers.CharField(source='election.title', read_only=True)
    voter_name = serializers.CharField(source='voter.voter_profile.first_name', read_only=True)
    
    class Meta:
        model = ElectionRegistration
        fields = ['id', 'election', 'status', 'registration_date', 
                 'election_title', 'voter_name']
    
    def create(self, validated_data):
        validated_data['voter'] = self.context['request'].user
        return super().create(validated_data)
