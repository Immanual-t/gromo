from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Skill, LearningProgress


# Define inline admin classes
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fieldsets = (
        ('Personal Info', {
            'fields': ('profile_pic', 'phone_number', 'city', 'state')
        }),
        ('Partner Details', {
            'fields': ('partner_id', 'partner_since', 'monthly_target', 'experience_level')
        }),
        ('Preferences', {
            'fields': ('preferred_products', 'notification_preferences')
        }),
    )


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 0
    max_num = 6


class LearningProgressInline(admin.TabularInline):
    model = LearningProgress
    extra = 0
    readonly_fields = ('last_activity',)


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, SkillInline, LearningProgressInline)
    list_display = (
    'username', 'email', 'first_name', 'last_name', 'is_staff', 'get_partner_id', 'get_experience_level')
    list_filter = ('is_staff', 'is_superuser', 'profile__experience_level')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'profile__partner_id')

    def get_partner_id(self, obj):
        return obj.profile.partner_id if hasattr(obj, 'profile') else None

    get_partner_id.short_description = 'Partner ID'

    def get_experience_level(self, obj):
        return obj.profile.get_experience_level_display() if hasattr(obj, 'profile') else None

    get_experience_level.short_description = 'Experience'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# Register standalone models
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_type', 'proficiency_level', 'last_assessed')
    list_filter = ('product_type', 'proficiency_level')
    search_fields = ('user__username', 'user__email')
    list_editable = ('proficiency_level',)
    date_hierarchy = 'last_assessed'


@admin.register(LearningProgress)
class LearningProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'module_name', 'completion_percentage', 'completed', 'last_activity')
    list_filter = ('completed', 'module_name')
    search_fields = ('user__username', 'user__email', 'module_name')
    list_editable = ('completion_percentage', 'completed')
    date_hierarchy = 'last_activity'