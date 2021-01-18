from os import sys
import requests as req
from time import sleep

RETRY_BACKOFF_FACTOR = 1
MAX_RETRY_COUNT = 5


class HttpRetry():

    def get(self, url, **kwargs):
        return self._retry(lambda: req.get(url, **kwargs))

    def put(self, url, **kwargs):
        return self._retry(lambda: req.put(url, **kwargs))

    def post(self, url, **kwargs):
        return self._retry(lambda: req.post(url, **kwargs))

    @staticmethod
    def sleep_time(count):
        return RETRY_BACKOFF_FACTOR * (2 ** count)

    def _retry(self, http_call):
        response = http_call()
        if response.status_code != 503:
            return response

        err_print("The HTTP call failed. Retrying...")
        for count in range(1, MAX_RETRY_COUNT + 1):
            sleep(self.sleep_time(count))
            response = http_call()
            if response.status_code != 503:
                return response
            else:
                self._log_retry_failure(count, response)

        raise req.exceptions.RetryError("TODO")

    def _log_retry_failure(self, count, response):
        err_print("Retry {}/{} failed, status={}{}".format(
            count,
            MAX_RETRY_COUNT,
            response.status_code,
            self._sleep_message(count)
        ))

    def _sleep_message(self, count):
        if count < MAX_RETRY_COUNT:
            return ", sleeping for {} seconds...".format(self.sleep_time(count))
        else:
            return ""


def err_print(message):
    print(message, file=sys.stderr, flush=True)


def total_sleep_time():
    return sum(HttpRetry().sleep_time(n) for n in range(0, MAX_RETRY_COUNT))


"""
Create a http requests object with an embedded retry strategy.
Affects only GET,PUT,POST requests whose response status is 503.
Intention is to hide small server downtimes during deployments.
The sleep duration between retries is [0,2,4,8,16] seconds.
Retries 5 times. The first retry is immediate.

The logged message does _not_ say 'Press Control^C to exit.'
because Control^C requires a runtime environment with a tty.
That would require a [docker run -it] which would fail in the
target environment, a CI pipeline, which invariably has no tty.
"""


"""
Superclass source and docs are here:
https://github.com/urllib3/urllib3/blob/master/src/urllib3/util/retry.py
https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry

I tried moving the kwargs in http_retry() into a LoggingRetry.__init__(...)
I got: TypeError: __init__() got an unexpected keyword argument
Don't know why, so for now they stay in http_retry()

Adding attributes to this class causes errors due, I think, to the Retry
super-class doing clever things with __init__(), new(), and __getattr__()
"""

""""
Retry documentation says the backoff algorithm is:
   {backoff factor} * (2 ** ({number of retries} - 1))
With backoff_factor==1, this would give successive sleeps of:
   [ 0.5, 1, 2, 4, 8, 16, ... ]
However, the _actual_ sleep durations you get from get_backoff_time() are:
   [ 0, 2, 4, 8, 16, ... ]
And empirically, before the first retry there is indeed no sleep.
So the first retry is happening immediately.
"""

