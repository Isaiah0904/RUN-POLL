
from django.contrib import admin
from .models import Election, Position, Candidate, ElectionRegistration

class PositionInline(admin.TabularInline):
    model = Position
    extra = 1

class CandidateInline(admin.TabularInline):
    model = Candidate
    extra = 0
    readonly_fields = ['vote_count', 'vote_percentage']

@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'start_date', 'end_date', 'total_votes', 'created_by']
    list_filter = ['status', 'results_visibility', 'start_date']
    search_fields = ['title', 'description']
    inlines = [PositionInline]
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new election
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['title', 'election', 'total_votes', 'max_candidates']
    list_filter = ['election']
    search_fields = ['title', 'election__title']
    inlines = [CandidateInline]

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['user', 'position', 'is_approved', 'vote_count', 'registration_date']
    list_filter = ['is_approved', 'position__election', 'registration_date']
    search_fields = ['user__username', 'user__email', 'position__title']
    readonly_fields = ['vote_count', 'vote_percentage']

@admin.register(ElectionRegistration)
class ElectionRegistrationAdmin(admin.ModelAdmin):
    list_display = ['voter', 'election', 'status', 'registration_date', 'approved_by']
    list_filter = ['status', 'election', 'registration_date']
    search_fields = ['voter__username', 'voter__email', 'election__title']
