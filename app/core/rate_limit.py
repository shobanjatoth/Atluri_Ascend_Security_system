import time
from collections import defaultdict
from threading import Lock

from app.core.config import settings


class RateLimiter:

    def __init__(
        self,
        max_requests: int,
        window_seconds: int,
    ):
        self.max_requests = max_requests
        self.window_seconds = window_seconds

        self.requests = defaultdict(list)

        self.lock = Lock()

    def is_allowed(self, client_ip: str) -> bool:

        current_time = time.time()

        with self.lock:

            request_times = self.requests[client_ip]

            valid_requests = []

            for request_time in request_times:

                if current_time - request_time < self.window_seconds:
                    valid_requests.append(request_time)

            self.requests[client_ip] = valid_requests

            if len(valid_requests) >= self.max_requests:
                return False

            self.requests[client_ip].append(current_time)

            return True


login_rate_limiter = RateLimiter(
    max_requests=settings.LOGIN_RATE_LIMIT,
    window_seconds=settings.LOGIN_RATE_WINDOW_SECONDS,
)


qr_rate_limiter = RateLimiter(
    max_requests=settings.QR_RATE_LIMIT,
    window_seconds=settings.QR_RATE_WINDOW_SECONDS,
)