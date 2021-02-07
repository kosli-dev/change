from .mock_file_fingerprinter import MockFingerprinter


class MockImageFingerprinter(MockFingerprinter):

    def _fingerprint_image(self, image_name):
        self._called = True
        if image_name == self._expected:
            return self._sha
        else:
            self._failed([
                f"Expected: image_name=={self._expected}",
                f"  Actual: image_name=={image_name}"
            ])

    @staticmethod
    def _function_sig():
        return "_fingerprint_image(filename)"
