from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from os import sys


RETRY_COUNT = 5
RETRY_BACKOFF_FACTOR = 1


def http_retry():
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
    https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry
    WARNING: Putting attributes in this class causes problems due to
    the Retry super-class doing tricky things with __getattr__

    The logged message does _not_ say 'Press Control^C to exit.'
    because Control^C requires a runtime environment with a tty.
    That would require the [docker run] calls to use the -it option.
    That would fail in the target environment, a CI pipeline, which
    invariably has no tty.
    """
    def increment(self, *args, **kwargs):
        self.log_increment()
        return super().increment(*args, **kwargs)

    def log_increment(self):
        count = len(self.history)
        if count == 0:
            # I can find no way to access the original
            # failed response we are retrying against :-(
            err_print("The HTTP call failed. Retrying...")
            return
        failed_request = self.history[-1]
        message = "Retry {}/{} failed, status={}{}".format(
            count,                    # 3
            RETRY_COUNT,              # 5
            failed_request.status,    # 503
            self.sleep_message(count)
            )
        err_print(message)

    def sleep_message(self, count):
        if count < RETRY_COUNT:
            return ", sleeping for {} seconds...".format(self.sleep_time(count))
        else:
            return ""

    @staticmethod
    def sleep_time(n):
        """"
        Retry documentation says the backoff algorithm is:
           {backoff factor} * (2 ** ({number of retries} - 1))
        With backoff_factor==1, this would give successive sleeps of:
           [ 0.5, 1, 2, 4, 8, 16, ... ]
        However, the _actual_ sleep durations you get are:
           [ 0, 2, 4, 8, 16, ... ]
        And empirically, before the first retry...
          o) there is indeed no sleep
          o) Retry.get_backoff_time() does indeed return zero
          o) So the range() in total_sleep_time() below starts at 1.
        """
        return RETRY_BACKOFF_FACTOR * (2 ** n)

    @staticmethod
    def total_sleep_time():
        total = sum(LoggingRetry.sleep_time(n) for n in range(1, RETRY_COUNT))
        return total


def err_print(message):
    # flush is handy for manual test run with capsys off
    print(message, file=sys.stderr, flush=True)
