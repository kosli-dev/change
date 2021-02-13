from fingerprinters import FileFingerprinter


class MockFileFingerprinter(FileFingerprinter):

    def __init__(self, image_name, digest):
        self.__expected = image_name
        self.__digest = digest
        self.__called = False

    def __enter__(self):
        return self

    def sha(self, string):
        self.__called = True
        assert self.handles_protocol(string)
        pathed_filename = string[len(self.protocol):]
        if pathed_filename == self.__expected:
            return self.__digest
        else:
            lines = [
                f"Expected: string=={self.__expected}",
                f"  Actual: string=={pathed_filename}",
            ]
            self.__failed(lines)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.__called:
            print(exc_type)
            print(exc_val)
            print(exc_tb)
            self.__failed(["Expected call did not happen"])

    def __failed(self, lines):
        message = "\n".join([
            f"{self.__class__.__name__}.sha(string)",
            "FAILED",
        ] + lines)
        raise RuntimeError(message)
