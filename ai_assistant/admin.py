from django.contrib import admin
from django.utils.html import format_html
from .models import Conversation, Message, AIResponse, LearningContent, SalesTemplate


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('role', 'content', 'created_at')


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'customer_type', 'product_type', 'created_at', 'message_count')
    list_filter = ('customer_type', 'product_type', 'created_at')
    search_fields = ('title', 'user__username', 'user__email')
    date_hierarchy = 'created_at'
    inlines = [MessageInline]

    def message_count(self, obj):
        return obj.messages.count()

    message_count.short_description = 'Messages'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'role', 'short_content', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('content', 'conversation__title', 'conversation__user__username')
    date_hierarchy = 'created_at'

    def short_content(self, obj):
        if len(obj.content) > 100:
            return obj.content[:100] + '...'
        return obj.content

    short_content.short_description = 'Content'


@admin.register(AIResponse)
class AIResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'request_type', 'created_at', 'short_prompt', 'short_response')
    list_filter = ('request_type', 'created_at')
    search_fields = ('prompt', 'response', 'user__username')
    date_hierarchy = 'created_at'

    def short_prompt(self, obj):
        if len(obj.prompt) > 100:
            return obj.prompt[:100] + '...'
        return obj.prompt

    short_prompt.short_description = 'Prompt'

    def short_response(self, obj):
        if len(obj.response) > 100:
            return obj.response[:100] + '...'
        return obj.response

    short_response.short_description = 'Response'


@admin.register(LearningContent)
class LearningContentAdmin(admin.ModelAdmin):
    list_display = ('topic', 'user', 'product_type', 'difficulty_level', 'created_at', 'is_read')
    list_filter = ('product_type', 'difficulty_level', 'is_read', 'created_at')
    search_fields = ('topic', 'content', 'summary', 'user__username')
    list_editable = ('is_read',)
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'topic', 'product_type', 'difficulty_level', 'is_read')
        }),
        ('Content', {
            'fields': ('summary', 'content')
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


@admin.register(SalesTemplate)
class SalesTemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'product_type', 'template_type', 'created_at')
    list_filter = ('product_type', 'template_type', 'created_at')
    search_fields = ('title', 'content', 'user__username')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'title', 'product_type', 'template_type')
        }),
        ('Content', {
            'fields': ('content',)
        }),
    )