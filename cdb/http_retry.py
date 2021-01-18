"""
Wraps http requests with a simple retry strategy.
Affects only GET,PUT,POST requests whose response status is 503.
Intention is to hide small server downtimes during deployments.
Retries 5 times with successive sleep durations of [1,2,4,8,16] seconds.

The logged message does _not_ say 'Press Control^C to exit.'
because Control^C requires a runtime environment with a tty.
That would require a [docker run -it] which would fail in the
target environment, a CI pipeline, which invariably has no tty.
"""

from os import sys
import requests as http
from time import sleep

RETRY_BACKOFF_FACTOR = 1
MAX_RETRY_COUNT = 5


class HttpRetry():
    """
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

    def get(self, url, **kwargs):
        return self._retry(lambda: http.get(url, **kwargs))

    def put(self, url, **kwargs):
        return self._retry(lambda: http.put(url, **kwargs))

    def post(self, url, **kwargs):
        return self._retry(lambda: http.post(url, **kwargs))

    @staticmethod
    def sleep_time(count):
        return RETRY_BACKOFF_FACTOR * (2 ** count)

    def _retry(self, http_call):
        response = http_call()
        status = response.status_code
        if status != 503:
            return response

        err_print("Response.status={}{}".format(status, self._sleep_message(0)))
        for count in range(1, MAX_RETRY_COUNT + 1):
            sleep(self.sleep_time(count))
            response = http_call()
            status = response.status_code
            if status != 503:
                # TODO: log message here
                return response
            else:
                self._log_retry_failed(count, status)

        raise http.exceptions.RetryError("TODO")

    def _log_retry_failed(self, count, status):
        err_print("Retry {}/{}: response.status={}{}".format(
            count,
            MAX_RETRY_COUNT,
            status,
            self._sleep_message(count)
        ))

    def _sleep_message(self, count):
        if count < MAX_RETRY_COUNT:
            return ", retrying in {} seconds...".format(self.sleep_time(count))
        else:
            return ""


def err_print(message):
    print(message, file=sys.stdout, flush=True)


def total_sleep_time():
    return sum(HttpRetry().sleep_time(n) for n in range(0, MAX_RETRY_COUNT))
