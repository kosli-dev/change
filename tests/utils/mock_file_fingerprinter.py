from fingerprinters import FileFingerprinter


class MockFileFingerprinter(FileFingerprinter):

    def __init__(self, image_name, digest):
        self._expected = image_name
        self._digest = digest
        self._called = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self._called:
            print(exc_type)
            print(exc_val)
            print(exc_tb)
            self._failed(["Expected call did not happen"])

    def sha(self, _protocol, image_name):
        self._called = True
        if image_name == self._expected:
            return self._digest
        else:
            lines = [
                f"Expected: artifact_name=={self._expected}",
                f"  Actual: artifact_name=={image_name}",
            ]
            self._failed(lines)

    def _failed(self, lines):
        message = "\n".join([
            f"{self.__class__.__name__}._fingerprint(artifact_name)",
            "FAILED",
        ] + lines)
        raise RuntimeError(message)
