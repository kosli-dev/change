from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from os import sys


RETRY_COUNT = 5
RETRY_BACKOFF_FACTOR = 1


def http_retry():
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
    strategy = LoggingRetry(
        total=RETRY_COUNT,
        backoff_factor=RETRY_BACKOFF_FACTOR,
        status_forcelist=[503],
        allowed_methods=["GET", "POST", "PUT"]
    )
    adapter = HTTPAdapter(max_retries=strategy)
    session = Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


class LoggingRetry(Retry):
    """
    Superclass source and docs are here:
    https://github.com/urllib3/urllib3/blob/master/src/urllib3/util/retry.py
    https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry

    I tried moving the kwargs in http_retry() into a LoggingRetry.__init__(...)
    I got: TypeError: __init__() got an unexpected keyword argument
    Don't know why, so for now they stay in http_retry()

    Adding attributes to this class causes error due, I think, to the Retry
    super-class doing clever things with __init__(), new(), and __getattr__()
    """
    def increment(self, *args, **kwargs):
        if self.count() == 0:
            err_print("The HTTP call failed. Retrying...")
        new_retry = super().increment(*args, **kwargs)
        new_retry.log_increment()
        return new_retry

    def log_increment(self):
        failed_request = self.history[-1]
        message = "Retry {}/{} failed, status={}{}".format(
            self.count(),
            RETRY_COUNT,
            failed_request.status,
            self.sleep_message()
        )
        err_print(message)

    def count(self):
        return len(self.history)

    def sleep_message(self):
        if self.count() < RETRY_COUNT:
            return ", sleeping for {} seconds...".format(self.sleep_time())
        else:
            return ""

    def sleep_time(self, n=None):
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
        if n is None:
            n = self.count()
        if n == 0:
            return 0
        else:
            return RETRY_BACKOFF_FACTOR * (2 ** n)


def total_sleep_time():
    return sum(LoggingRetry().sleep_time(n) for n in range(0, RETRY_COUNT))


def err_print(message):
    # flush is handy for manual test run with capsys off
    print(message, file=sys.stderr, flush=True)
