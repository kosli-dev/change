from fingerprinters import DockerFingerprinter


class MockDockerFingerprinter(DockerFingerprinter):

    def __init__(self, string, digest):
        self.__expected = string
        self.__digest = digest
        self.__called = False

    def __enter__(self):
        return self

    def sha(self, string):
        self.__called = True
        image_name = self.artifact_name(string)
        if image_name == self.__expected:
            return self.__digest
        else:
            lines = [
                f"Expected: string=={self.__expected}",
                f"  Actual: string=={image_name}",
            ]
            self.__failed(lines)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.__called:
            import traceback
            traceback.print_tb(exc_tb)
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
