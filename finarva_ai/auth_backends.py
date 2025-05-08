# File location: finarva_ai/auth_backends.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from finarva_ai.request_middleware import RequestMiddleware

User = get_user_model()


class AdminBackend(ModelBackend):
    """
    Authentication backend for admin users that maintains session separation.
    This backend only processes authentication for admin paths and ensures
    admin users don't get confused with frontend users.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        # If not specified, get current request from middleware
        if not request:
            request = RequestMiddleware.get_current_request()

        # If this is not an admin request, don't process it
        if not request or not getattr(request, 'is_admin_request', False):
            return None

        try:
            user = User.objects.get(username=username)
            # Only authenticate staff users for admin
            if user.check_password(password) and user.is_staff:
                return user
        except User.DoesNotExist:
            return None

        return None

    def get_user(self, user_id):
        """
        Override get_user to always return None if not in an admin context,
        preventing admin users from being loaded in frontend contexts.
        """
        # Check if this is an admin request using the middleware
        is_admin_context = RequestMiddleware.is_admin_request()

        # If not an admin context, don't return the user
        if not is_admin_context:
            return None

        # Proceed with normal user retrieval for admin context
        return super().get_user(user_id)


class RegularUserBackend(ModelBackend):
    """
    Authentication backend for regular users.
    This ensures frontend users don't get confused with admin users.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        # If not specified, get current request from middleware
        if not request:
            request = RequestMiddleware.get_current_request()

        # If this is an admin request, don't process it
        if request and getattr(request, 'is_admin_request', False):
            return None

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

        return None

    def get_user(self, user_id):
        """
        Override get_user to always return None if in an admin context,
        preventing frontend users from being loaded in admin contexts.
        """
        # Check if this is an admin request using the middleware
        is_admin_context = RequestMiddleware.is_admin_request()

        # If this is an admin context, don't return the user
        if is_admin_context:
            return None

        # Proceed with normal user retrieval for frontend context
        return super().get_user(user_id)