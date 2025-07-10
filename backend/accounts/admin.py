
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, VoterProfile, AdminProfile

class VoterProfileInline(admin.StackedInline):
    model = VoterProfile
    can_delete = False

class AdminProfileInline(admin.StackedInline):
    model = AdminProfile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'user_type', 'is_active', 'is_verified', 'date_joined']
    list_filter = ['user_type', 'is_active', 'is_verified', 'date_joined']
    search_fields = ['email', 'username']
    ordering = ['email']
    
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type', 'is_verified')}),
    )
    
    def get_inlines(self, request, obj):
        if obj and obj.user_type == 'voter':
            return [VoterProfileInline]
        elif obj and obj.user_type == 'admin':
            return [AdminProfileInline]
        return []

admin.site.register(User, CustomUserAdmin)
admin.site.register(VoterProfile)
admin.site.register(AdminProfile)
