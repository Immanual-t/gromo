# File location: finarva_ai/session_middleware.py

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
import threading
from finarva_ai.request_middleware import RequestMiddleware

# Use thread-local storage to avoid global state issues
_local = threading.local()


class SeparateAdminSessionMiddleware(MiddlewareMixin):
    """
    Enhanced middleware to completely separate admin and frontend sessions
    using distinct cookie names, paths, and enforced request context.
    """

    def process_request(self, request):
        """
        Configure session settings based on request path
        and preserve original settings
        """
        # Store original cookie settings in thread-local storage
        if not hasattr(_local, 'original_settings'):
            _local.original_settings = {
                'session_cookie_name': settings.SESSION_COOKIE_NAME,
                'csrf_cookie_name': settings.CSRF_COOKIE_NAME,
                'session_cookie_path': getattr(settings, 'SESSION_COOKIE_PATH', '/'),
                'csrf_cookie_path': getattr(settings, 'CSRF_COOKIE_PATH', '/')
            }

        # Determine if the request is for the admin site
        is_admin = request.path.startswith('/admin/')

        # Set the appropriate flag on the request
        request.is_admin_request = is_admin

        if is_admin:
            # Use admin-specific cookie settings
            settings.SESSION_COOKIE_NAME = 'finarva_admin_sessionid'
            settings.CSRF_COOKIE_NAME = 'finarva_admin_csrftoken'
            settings.SESSION_COOKIE_PATH = '/admin/'
            settings.CSRF_COOKIE_PATH = '/admin/'
        else:
            # Use frontend-specific cookie settings
            settings.SESSION_COOKIE_NAME = 'finarva_sessionid'
            settings.CSRF_COOKIE_NAME = 'finarva_csrftoken'
            settings.SESSION_COOKIE_PATH = '/'
            settings.CSRF_COOKIE_PATH = '/'

    def process_response(self, request, response):
        """
        Restore original settings and ensure cookies have the right paths
        """
        try:
            # Fix any existing cookies in the response
            if hasattr(request, 'is_admin_request'):
                # For admin responses, ensure admin cookies have /admin/ path
                if request.is_admin_request:
                    self._fix_cookie_paths(response, '/admin/')
                else:
                    # For frontend responses, ensure frontend cookies have / path
                    self._fix_cookie_paths(response, '/')

            # Restore original settings if we stored them
            if hasattr(_local, 'original_settings'):
                settings.SESSION_COOKIE_NAME = _local.original_settings['session_cookie_name']
                settings.CSRF_COOKIE_NAME = _local.original_settings['csrf_cookie_name']
                settings.SESSION_COOKIE_PATH = _local.original_settings['session_cookie_path']
                settings.CSRF_COOKIE_PATH = _local.original_settings['csrf_cookie_path']
        except Exception:
            # Ensure settings get restored even if there's an error
            if hasattr(_local, 'original_settings'):
                settings.SESSION_COOKIE_NAME = _local.original_settings['session_cookie_name']
                settings.CSRF_COOKIE_NAME = _local.original_settings['csrf_cookie_name']

        return response

    def process_exception(self, request, exception):
        """Restore original settings even if there's an exception"""
        if hasattr(_local, 'original_settings'):
            settings.SESSION_COOKIE_NAME = _local.original_settings['session_cookie_name']
            settings.CSRF_COOKIE_NAME = _local.original_settings['csrf_cookie_name']
            settings.SESSION_COOKIE_PATH = _local.original_settings['session_cookie_path']
            settings.CSRF_COOKIE_PATH = _local.original_settings['csrf_cookie_path']
        return None

    def _fix_cookie_paths(self, response, path):
        """
        Ensures all cookies in the response have the correct path.
        This fixes cases where Django might not set the path correctly.
        """
        if not hasattr(response, 'cookies'):
            return

        # Define which cookies should have which path
        admin_cookies = ['finarva_admin_sessionid', 'finarva_admin_csrftoken',
                         'admin_logged_in', 'finarva_admin_auth']
        frontend_cookies = ['finarva_sessionid', 'finarva_csrftoken']

        for cookie_name, cookie in response.cookies.items():
            if path == '/admin/' and cookie_name in admin_cookies:
                cookie['path'] = '/admin/'
            elif path == '/' and cookie_name in frontend_cookies:
                cookie['path'] = '/'