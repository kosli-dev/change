from commands import Fingerprinter


class MockFileFingerprinter(Fingerprinter):
    def __init__(self, expected, sha):
        self._expected = expected
        self._sha = sha
        self._called = False

    def __enter__(self):
        return self

    def _fingerprint_file(self, filename):
        self._called = True
        if filename == self._expected:
            return self._sha
        else:
            message = "\n".join([
                self.MY_NAME,
                f"FAILED",
                f"Expected: filename=={self._expected}",
                f"  Actual: filename=={filename}"
            ])
            raise RuntimeError(message)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self._called:
            message = "\n".join([
                self.MY_NAME,
                f"FAILED",
                f"Expected call did not happen",
            ])
            raise RuntimeError(message)

    MY_NAME = 'MockFileFingerprinter._fingerprint_file(filename)'
