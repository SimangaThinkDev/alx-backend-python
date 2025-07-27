from datetime import datetime, time
import logging
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from django.http import JsonResponse
from django.http import HttpResponseForbidden

logging.basicConfig(
    filename="requests.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)

logger = logging.getLogger("requests.log")
logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    # One-time configuration and initialization.

    def __call__(self, request):
        response = self.get_response(request)
        user = request.user
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")

        # Code to be executed for each request/response after
        # the view is called.

        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.deadline = time(21)
        self.start = time(18)

    def __call__(self, request):
        now = datetime.datetime.now()
        user = request.user
        response = self.get_response(request)

        if not self.in_between(now):
            response = HttpResponseForbidden("Time out of service time")

        return response

    def in_between(self, check_time):
        return self.start <= check_time <= self.deadline


class OffensiveLanguageMiddleware(MiddlewareMixin):
    RATE_LIMIT = 5
    TIME_PERIOD = 60  # in seconds

    def __init__(self, get_response):
        super.__init__()
        self.get_response = get_response

    def __call__(self, request):
        super.__call__()

        ip = self.get_client_ip(request)
        key = f"rate-limit-{ip}"

        request_count = cache.get(key, 0)

        if request_count is None:
            cache.set(key, 0, timeout=self.TIME_PERIOD)
            request_count = 0

        if request_count >= self.RATE_LIMIT:
            return JsonResponse({"error": "Rate limit exceeded"}, status=429)

        cache.incr(key)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.response = get_response

    """ If the user is not admin or moderator,
    it should return error 403 """

    def __call__(self, request):
        if request.user.is_authenticated():
            if not request.user.is_admin and not request.user.is_moderator:
                response = HttpResponseForbidden("Access denied")
        return response
