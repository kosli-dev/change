from .mock_fingerprinter import MockFingerprinter


class MockFileFingerprinter(MockFingerprinter):

    def _fingerprint_file(self, filename):
        self._called = True
        if filename == self._expected:
            return self._sha
        else:
            self._failed([
                f"Expected: filename=={self._expected}",
                f"  Actual: filename=={filename}"
            ])

    @staticmethod
    def _function_sig():
        return "_fingerprint_file(filename)"
