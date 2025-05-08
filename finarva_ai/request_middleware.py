# File location: finarva_ai/request_middleware.py

import threading
import uuid
from django.utils.deprecation import MiddlewareMixin


class RequestMiddleware(MiddlewareMixin):
    """
    Enhanced middleware that stores the request object in thread local storage
    with better handling of concurrent requests and context persistence.
    """
    # Thread local storage with request map
    thread_local = threading.local()

    @classmethod
    def _init_thread_data(cls):
        """Initialize thread local storage if needed"""
        if not hasattr(cls.thread_local, 'requests'):
            cls.thread_local.requests = {}
            cls.thread_local.current_request_id = None

    def process_request(self, request):
        """
        Store request in thread local storage with a unique ID
        and mark if it's an admin request
        """
        RequestMiddleware._init_thread_data()

        # Generate a unique ID for this request
        request_id = str(uuid.uuid4())

        # Determine if this is an admin request
        is_admin = request.path.startswith('/admin/')

        # Store the admin status on the request object
        request.is_admin_request = is_admin

        # Store the request in thread local storage
        RequestMiddleware.thread_local.requests[request_id] = request
        RequestMiddleware.thread_local.current_request_id = request_id

        # Store the request ID on the request itself for retrieval
        request.request_id = request_id

    def process_response(self, request, response):
        """Clean up thread local storage for this request"""
        try:
            if hasattr(request, 'request_id'):
                request_id = request.request_id
                if hasattr(RequestMiddleware.thread_local,
                           'requests') and request_id in RequestMiddleware.thread_local.requests:
                    del RequestMiddleware.thread_local.requests[request_id]

                # Clear current request ID if it matches
                if hasattr(RequestMiddleware.thread_local,
                           'current_request_id') and RequestMiddleware.thread_local.current_request_id == request_id:
                    RequestMiddleware.thread_local.current_request_id = None
        except Exception:
            # Fail silently - cleanup issues shouldn't affect response
            pass

        return response

    def process_exception(self, request, exception):
        """Clean up thread local storage even if there's an exception"""
        try:
            if hasattr(request, 'request_id'):
                request_id = request.request_id
                if hasattr(RequestMiddleware.thread_local,
                           'requests') and request_id in RequestMiddleware.thread_local.requests:
                    del RequestMiddleware.thread_local.requests[request_id]

                # Clear current request ID if it matches
                if hasattr(RequestMiddleware.thread_local,
                           'current_request_id') and RequestMiddleware.thread_local.current_request_id == request_id:
                    RequestMiddleware.thread_local.current_request_id = None
        except Exception:
            # Fail silently - cleanup issues shouldn't affect exception handling
            pass

        return None

    @classmethod
    def get_current_request(cls):
        """Get the current request from thread local storage"""
        cls._init_thread_data()

        current_id = getattr(cls.thread_local, 'current_request_id', None)
        if current_id and current_id in cls.thread_local.requests:
            return cls.thread_local.requests[current_id]

        return None

    @classmethod
    def is_admin_request(cls):
        """Helper method to check if current request is an admin request"""
        request = cls.get_current_request()
        return request and getattr(request, 'is_admin_request', False)