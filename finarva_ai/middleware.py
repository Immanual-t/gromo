# Create a new file: finarva_ai/middleware.py
from django.utils.deprecation import MiddlewareMixin

class AdminAuthMiddleware(MiddlewareMixin):
    """
    Middleware to separate admin and user authentication
    """
    def process_request(self, request):
        if request.path.startswith('/admin/'):
            # Only check admin auth cookie for admin URLs
            if not request.COOKIES.get('finarva_admin_auth') == 'true' and request.user.is_authenticated:
                # If a user is logged in but not as admin, log them out for admin pages
                # This doesn't affect their session elsewhere
                request.admin_user_conflict = True
        return None