import cdb.http_retry as http_retry


def retry_backoff_factor(f):
    return RetryBackOffFactor(f)


class RetryBackOffFactor(object):
    def __init__(self, factor):
        self._factor = factor

    def __enter__(self):
        self._original = http_retry.RETRY_BACKOFF_FACTOR
        http_retry.RETRY_BACKOFF_FACTOR = self._factor

    def __exit__(self, _type, _value, _traceback):
        http_retry.RETRY_BACKOFF_FACTOR = self._original
