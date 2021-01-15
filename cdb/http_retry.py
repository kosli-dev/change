from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from os import sys


RETRY_COUNT = 5
RETRY_BACKOFF_FACTOR = 1


def http_retry():
    retry = LoggingRetry(
        total=RETRY_COUNT,
        backoff_factor=RETRY_BACKOFF_FACTOR,
        status_forcelist=[503],
        allowed_methods=["POST"]
    )
    adapter = HTTPAdapter(max_retries=retry)
    s = Session()
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    return s


class LoggingRetry(Retry):
    """
    https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry
    Note: Don't put any attributes in this class!
    The Retry subclass is doing tricky things with __getattr__
    """
    def increment(self, *args, **kwargs):
        self.log_increment(**kwargs)
        return super().increment(*args, **kwargs)

    def log_increment(self, **kwargs):
        count = self.retry_count()
        if count == 0:
            return
        if count == 1:
            self.log_original_http_call_failed(**kwargs)
        if count > 1:
            self.log_previous_retry_failed()
        if count < RETRY_COUNT:
            self.log_retrying_in_n_seconds()

    def log_original_http_call_failed(self, **kwargs):
        request = self.failed_request()
        # request.url (a string) contains only the path :(
        pool = kwargs['_pool']
        path = request.url
        url = "{}://{}:{}{}".format(pool.scheme, pool.host, pool.port, path)
        self.err_print("{} failed".format(request.method))  # eg POST
        self.err_print("URL={}".format(url))
        self.err_print("STATUS={}".format(request.status))

    def log_previous_retry_failed(self):
        self.err_print('failed')

    def log_retrying_in_n_seconds(self):
        """
        The printed message does _not_ say 'Press Control^C to exit.'
        For this to work the program environment needs a tty, but the
        target environment is a CI pipeline which invariably has no tty.
        """
        message = "Retrying in {} seconds ({}/{})...".format(
            self.next_backoff_time(),
            self.retry_count(),
            RETRY_COUNT - 1
            )
        self.err_print(message, end='')

    def retry_count(self):
        return len(self.history)

    def failed_request(self):
        return self.history[-1]

    def next_backoff_time(self):
        return self.backoff_time(self.retry_count())

    def total_backoff_time(self):
        return sum(self.backoff_time(n) for n in range(0, RETRY_COUNT))

    @staticmethod
    def backoff_time(n):
        """"
        Retry documentation says the backoff algorithm is:
           {backoff factor} * (2 ** ({number of retries} - 1))
        With backoff_factor==1, this would give successive sleeps of:
           [ 0.5, 1, 2, 4, 8, 16, 32, ... ]
        However, self.get_backoff_time() _actually_ returns:
           [ 0, 2, 4, 8, 16, 32, ... ]
        Empirically, this _is_ the forthcoming sleep duration.
        The [0] is the _original_ http call, so zero never appears
        in a log message (where it would look strange).
        The first retry sleep is [2], the second is [4] etc.
        """
        return RETRY_BACKOFF_FACTOR * (2 ** n)

    @staticmethod
    def err_print(message, **kwargs):
        print(message, **dict(kwargs, file=sys.stderr, flush=True))
