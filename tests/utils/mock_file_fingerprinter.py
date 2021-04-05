from fingerprinters import FileFingerprinter


class MockFileFingerprinter(FileFingerprinter):

    def __init__(self, filename, digest):
        self.__expected = filename
        self.__digest = digest
        self.__called = False

    def __enter__(self):
        return self

    def sha(self, string):
        self.__called = True
        pathed_filename = self.artifact_name(string)
        if pathed_filename == self.__expected:
            return self.__digest
        else:
            lines = [
                f"Expected: string=={self.__expected}",
                f"  Actual: string=={pathed_filename}",
            ]
            self.__failed(lines)

    def __exit__(self, exc_type, exc_val, _exc_tb):
        if not self.__called:
            self.__failed([
                "Expected sha() call did not happen",
                f"exc_type = {exc_type}",
                f"exc_val = {exc_val}"
            ])

    def __failed(self, lines):
        message = "\n".join([
            f"{self.__class__.__name__}.sha(string)",
            "FAILED",
        ] + lines)
        raise RuntimeError(message)
