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

    def sha(self, pathed_filename):
        self._called = True
        if pathed_filename == self._expected:
            return self._digest
        else:
            lines = [
                f"Expected: pathed_filename=={self._expected}",
                f"  Actual: pathed_filename=={pathed_filename}",
            ]
            self._failed(lines)

    def _failed(self, lines):
        message = "\n".join([
            f"{self.__class__.__name__}.sha(pathed_filename)",
            "FAILED",
        ] + lines)
        raise RuntimeError(message)
