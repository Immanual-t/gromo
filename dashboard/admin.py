from django.contrib import admin
from django.db.models import Sum, Count
from django.utils.html import format_html
from .models import SalesPerformance, PerformanceGoal, AIInsight, CustomerLead


@admin.register(SalesPerformance)
class SalesPerformanceAdmin(admin.ModelAdmin):
    list_display = (
    'user', 'date', 'product', 'customer_name', 'amount', 'commission', 'product_category', 'lead_source')
    list_filter = ('date', 'product_category', 'lead_source', 'customer_type')
    search_fields = ('user__username', 'product', 'customer_name', 'notes')
    date_hierarchy = 'date'
    readonly_fields = ('commission',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'date', 'product', 'product_category')
        }),
        ('Customer Information', {
            'fields': ('customer_name', 'customer_type')
        }),
        ('Financial Details', {
            'fields': ('amount', 'commission')
        }),
        ('Additional Information', {
            'fields': ('lead_source', 'notes')
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


# In dashboard/admin.py

@admin.register(PerformanceGoal)
class PerformanceGoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'month_year', 'target_amount', 'target_customers', 'achievement_percentage_display')
    list_filter = ('month', 'year')
    search_fields = ('user__username',)

    def month_year(self, obj):
        return "{}/{}".format(obj.month, obj.year)

    month_year.short_description = 'Month/Year'

    def achievement_percentage_display(self, obj):
        percentage = obj.get_achieved_percentage()
        if percentage < 33:
            return '<span style="color: red;">{:.1f}%</span>'.format(percentage)
        elif percentage < 66:
            return '<span style="color: orange;">{:.1f}%</span>'.format(percentage)
        else:
            return '<span style="color: green;">{:.1f}%</span>'.format(percentage)

    achievement_percentage_display.short_description = 'Achievement'
    achievement_percentage_display.allow_tags = True  # This tells Django the field contains HTML


@admin.register(AIInsight)
class AIInsightAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'short_insight', 'created_at', 'is_read')
    list_filter = ('category', 'is_read', 'created_at')
    search_fields = ('user__username', 'insight_text')
    list_editable = ('is_read',)
    date_hierarchy = 'created_at'

    def short_insight(self, obj):
        if len(obj.insight_text) > 100:
            return obj.insight_text[:100] + '...'
        return obj.insight_text

    short_insight.short_description = 'Insight'


@admin.register(CustomerLead)
class CustomerLeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'phone', 'email', 'interest', 'status', 'priority_score', 'created_at')
    list_filter = ('status', 'interest', 'lead_source')
    search_fields = ('name', 'phone', 'email', 'user__username', 'notes')
    list_editable = ('status', 'priority_score')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'phone', 'email')
        }),
        ('Lead Details', {
            'fields': ('lead_source', 'interest', 'status', 'priority_score')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)