# https://github.com/LabD/django-session-timeout/
import time

from django.conf import settings
from django.shortcuts import redirect

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


SESSION_TIMEOUT_KEY = '_session_init_timestamp_'


class SessionTimeoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not hasattr(request, 'session') or request.session.is_empty():
            return

        init_time = request.session.setdefault(SESSION_TIMEOUT_KEY, time.time())
        expire_seconds = getattr(
            settings, 'SESSION_EXPIRE_SECONDS', settings.SESSION_COOKIE_AGE)

        session_is_expired = time.time() - init_time > expire_seconds

        if session_is_expired:
            request.session.flush()
            return redirect('/')
