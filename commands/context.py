import os
from .fingerprinter import Fingerprinter


class Context:
    """
    Holds (some) external dependencies to make Classic style testing easier.
    """
    def __init__(self, fingerprinter=None):
        if fingerprinter is None:
            self._fingerprinter = Fingerprinter()
        else:
            self._fingerprinter = fingerprinter

    @property
    def env(self):
        return os.environ

    def sha_digest_for_file(self, pathed_filename):
        return self._fingerprinter.of_file(pathed_filename)

    def sha_digest_for_docker_image(self, docker_image_name):
        return self._fingerprinter.of_docker_image(docker_image_name)

