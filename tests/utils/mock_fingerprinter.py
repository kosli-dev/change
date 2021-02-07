
class MockFingerprinter:
    def __init__(self, expected, sha):
        self._expected = expected
        self._sha = sha
        self._called = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self._called:
            self._failed(["Expected call did not happen"])

    def _fingerprint(self, artifact_name):
        self._called = True
        if artifact_name == self._expected:
            return self._sha
        else:
            self._failed([
                f"Expected: artifact_name=={self._expected}",
                f"  Actual: artifact_name=={artifact_name}"
            ])

    def _failed(self, lines):
        prefix = [
            f"{self.__class__.__name__}._fingerprint(artifact_name)",
            "FAILED"
        ]
        raise RuntimeError("\n".join(prefix + lines))
