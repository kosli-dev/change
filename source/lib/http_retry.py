"""
Wraps http requests with a simple retry strategy.
Affects only GET,PUT,POST requests whose response status is 503.
Intention is to hide small server downtimes during deployments.
Retries 5 times with successive sleep durations of [1,2,4,8,16] seconds.

The logged message does _not_ say 'Press Control^C to exit.'
because Control^C requires a runtime environment with a tty.
That would require a [docker run -it] which would fail in the
target environment, a CI pipeline, which invariably has no tty.

Originally we implemented http retries with this Retry class:
https://github.com/urllib3/urllib3/blob/master/src/urllib3/util/retry.py
https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry
We soon abandoned it.
- The only way we could mock the deeply occurring http calls was with httpretty
  which mocks at the socket level and has no way to mock only the
  first N calls in a retry situation. Thus it was impossible to test
  the happy-path scenario of a few 503's followed by a 200/201.
- It proved impossible create a Retry subclass containing attributes because
  of clever meta-programming in its __init__, new, and __getattr__
- Its empirical behaviour differed from its limited documented behaviour.
  Eg, its sleep backoff actually had _no_ sleep before the first retry.
- Its implementation was hard to understand.
  Eg, its crucial increment() method returned a _new_ Retry() object.
- In short, it was complicated and hard to test.
"""

from errors import ChangeError
import requests as http
from time import sleep

RETRY_BACKOFF_FACTOR = 1
MAX_RETRY_COUNT = 5


class HttpRetryExhausted(ChangeError):
    def __init__(self, url):
        self._url = url

    def url(self):
        return self._url


class HttpRetry():
    def __init__(self, stdout):
        self._status_retry_list = [503]
        self._max_count = MAX_RETRY_COUNT
        self._stdout = stdout

    def total_sleep_time(self):
        return sum(self._sleep_time(n) for n in range(0, self._max_count))

    def get(self, url, **kwargs):
        return self._http_retry(url, lambda: http.get(url, **kwargs))

    def put(self, url, **kwargs):
        return self._http_retry(url, lambda: http.put(url, **kwargs))

    def post(self, url, **kwargs):
        return self._http_retry(url, lambda: http.post(url, **kwargs))

    def _http_retry(self, url, http_call):
        response = http_call()
        status = response.status_code
        if not self._retry(status):
            return response
        count = 0
        seconds = self._sleep_time(count)
        self._log(count, status, seconds)
        for count in range(1, self._max_count + 1):
            seconds = self._sleep_time(count)
            sleep(seconds)
            response = http_call()
            status = response.status_code
            self._log(count, status, seconds)
            if not self._retry(status):
                return response

        raise HttpRetryExhausted(url)

    def _retry(self, status):
        return status in self._status_retry_list

    def _log(self, count, status, seconds):
        lhs = self._response_message(count, status)
        rhs = self._retry_message(count, status, seconds)
        self._stdout.print(f"{lhs}{rhs}")

    def _response_message(self, count, status):
        if count == 0:
            return f"Response.status={status}"
        else:
            return f"Retry {count}/{self._max_count}: response.status={status}"

    def _retry_message(self, count, status, seconds):
        if not self._retry(status):
            return ""
        elif count < self._max_count:
            return f", retrying in {seconds} seconds..."
        else:
            return ""

    @staticmethod
    def _sleep_time(count):
        return RETRY_BACKOFF_FACTOR * (2 ** count)

