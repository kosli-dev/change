from commands import Fingerprinter


class MockFingerprinter(Fingerprinter):
    def __init__(self, expected, sha):
        self._expected = expected
        self._sha = sha
        self._called = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self._called:
            self._failed(["Expected call did not happen"])

    def _failed(self, lines):
        prefix = [
            f"{self.__class__.__name__}._{self._function_sig()}",
            "FAILED"
        ]
        raise RuntimeError("\n".join(prefix + lines))
