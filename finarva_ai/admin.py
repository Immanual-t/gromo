# File location: finarva_ai/admin.py

from django.contrib.admin import AdminSite
from django.template.response import TemplateResponse
from django.contrib.auth.models import User, Group
from django.db.models import Count, Sum
from dashboard.models import SalesPerformance, CustomerLead, AIInsight, PerformanceGoal
from accounts.models import UserProfile
from ai_assistant.models import Conversation, Message, AIResponse, LearningContent, SalesTemplate
from django.utils import timezone
from datetime import timedelta
from django.contrib.sites.models import Site
from django.contrib.sites.admin import SiteAdmin
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.urls import reverse
from accounts.admin import UserAdmin as CustomUserAdmin
from django.contrib.auth.admin import GroupAdmin
from dashboard.admin import SalesPerformanceAdmin, PerformanceGoalAdmin, AIInsightAdmin, CustomerLeadAdmin
from ai_assistant.admin import ConversationAdmin, MessageAdmin, AIResponseAdmin, LearningContentAdmin, \
    SalesTemplateAdmin
from django.conf import settings
from django.contrib.auth.views import LoginView


class FinArvaAdminSite(AdminSite):
    site_header = 'FinArva AI Administration'
    site_title = 'FinArva AI Admin'
    index_title = 'Administration Portal'

    def has_permission(self, request):
        """Check if user has permission to access admin site"""
        # First, check cookies for quick authentication
        if request.COOKIES.get('finarva_admin_auth') == 'true' or request.COOKIES.get('admin_logged_in') == 'true':
            return True
        # Then fall back to normal permission check
        return super().has_permission(request)

    @method_decorator(never_cache)
    def login(self, request, extra_context=None):
        """
        Custom login view with dual cookie support for authentication and
        strict session isolation between admin and frontend.
        """
        # Mark this request as an admin request
        request.is_admin_request = True

        # Set session cookie name for admin login
        settings.SESSION_COOKIE_NAME = 'finarva_admin_sessionid'
        settings.CSRF_COOKIE_NAME = 'finarva_admin_csrftoken'

        # Make sure SESSION_COOKIE_PATH is set for admin
        settings.SESSION_COOKIE_PATH = '/admin/'

        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()

                # Only allow staff users
                if not user.is_staff:
                    form.add_error(None, "You don't have permission to access the admin site.")
                    context = {
                        'title': 'Log in',
                        'app_path': request.get_full_path(),
                        'form': form,
                        **(extra_context or {})
                    }
                    return TemplateResponse(request, 'admin/login.html', context)

                # Login the user with a session specific to admin
                auth_login(request, user)

                # Get the next URL from request GET parameters or default to admin index
                next_url = request.GET.get('next', '/admin/')
                if not next_url.startswith('/admin/'):
                    next_url = '/admin/'

                # Create response with direct URL redirect
                response = HttpResponseRedirect(next_url)

                # Set cookies for quick authentication on future requests
                response.set_cookie('admin_logged_in', 'true', max_age=3600 * 24 * 7, path='/admin/')
                response.set_cookie('finarva_admin_auth', 'true', max_age=3600 * 24 * 7, path='/admin/')

                return response

        # Fallback to default login for GET or failed POST
        context = {
            'title': 'Log in',
            'app_path': request.get_full_path(),
            **(extra_context or {})
        }

        return TemplateResponse(request, 'admin/login.html', context)

    @method_decorator(never_cache)
    def logout(self, request, extra_context=None):
        """
        Custom logout: clears admin cookies and logs out admin user
        without affecting frontend session.
        """
        # Mark this as an admin request
        request.is_admin_request = True

        # Set the right cookie names for admin
        settings.SESSION_COOKIE_NAME = 'finarva_admin_sessionid'
        settings.CSRF_COOKIE_NAME = 'finarva_admin_csrftoken'

        # Do the logout
        auth_logout(request)

        # Redirect to admin login
        response = HttpResponseRedirect('/admin/login/')

        # Clear the admin cookies
        response.delete_cookie('admin_logged_in', path='/admin/')
        response.delete_cookie('finarva_admin_auth', path='/admin/')
        response.delete_cookie('finarva_admin_sessionid', path='/admin/')
        response.delete_cookie('finarva_admin_csrftoken', path='/admin/')

        return response

    def get_app_list(self, request):
        """Custom app ordering in admin sidebar"""
        app_list = super().get_app_list(request)
        app_order = {
            'dashboard': 1,
            'ai_assistant': 2,
            'accounts': 3,
            'auth': 4,
        }
        app_list.sort(key=lambda x: app_order.get(x['app_label'], 10))
        return app_list

    def index(self, request, extra_context=None):
        """Custom admin index with dashboard stats"""
        # Mark this as an admin request
        request.is_admin_request = True

        today = timezone.now().date()
        start_date = today - timedelta(days=30)

        total_users = User.objects.count()
        active_users = User.objects.filter(last_login__gte=start_date).count()

        total_sales = SalesPerformance.objects.filter(date__gte=start_date).count()
        total_sales_amount = SalesPerformance.objects.filter(date__gte=start_date).aggregate(sum=Sum('amount'))[
                                 'sum'] or 0
        total_commission = SalesPerformance.objects.filter(date__gte=start_date).aggregate(sum=Sum('commission'))[
                               'sum'] or 0

        product_distribution = SalesPerformance.objects.filter(date__gte=start_date).values(
            'product_category').annotate(count=Count('id')).order_by('-count')

        total_leads = CustomerLead.objects.count()
        new_leads = CustomerLead.objects.filter(status='new').count()
        contacted_leads = CustomerLead.objects.filter(status='contacted').count()
        interested_leads = CustomerLead.objects.filter(status='interested').count()
        converted_leads = CustomerLead.objects.filter(status='converted').count()

        total_insights = AIInsight.objects.count()
        total_responses = AIInsight.objects.count()

        recent_sales = SalesPerformance.objects.all().order_by('-date')[:10]
        recent_leads = CustomerLead.objects.all().order_by('-created_at')[:10]

        context = {
            'title': 'FinArva AI Admin Dashboard',
            'total_users': total_users,
            'active_users': active_users,
            'total_sales': total_sales,
            'total_sales_amount': total_sales_amount,
            'total_commission': total_commission,
            'product_distribution': product_distribution,
            'total_leads': total_leads,
            'new_leads': new_leads,
            'contacted_leads': contacted_leads,
            'interested_leads': interested_leads,
            'converted_leads': converted_leads,
            'total_insights': total_insights,
            'total_responses': total_responses,
            'recent_sales': recent_sales,
            'recent_leads': recent_leads,
            'start_date': start_date,
            'today': today
        }

        if extra_context:
            context.update(extra_context)

        return super().index(request, context)


# Instantiate the custom admin site
admin_site = FinArvaAdminSite(name='finarva_admin')

# Register all required models to the custom admin site
admin_site.register(User, CustomUserAdmin)
admin_site.register(Group, GroupAdmin)
admin_site.register(SalesPerformance, SalesPerformanceAdmin)
admin_site.register(PerformanceGoal, PerformanceGoalAdmin)
admin_site.register(AIInsight, AIInsightAdmin)
admin_site.register(CustomerLead, CustomerLeadAdmin)
admin_site.register(Conversation, ConversationAdmin)
admin_site.register(Message, MessageAdmin)
admin_site.register(AIResponse, AIResponseAdmin)
admin_site.register(LearningContent, LearningContentAdmin)
admin_site.register(SalesTemplate, SalesTemplateAdmin)
admin_site.register(Site, SiteAdmin)