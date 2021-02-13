import os
from fingerprinters import *


class Context:
    """
    Holds (some) external dependencies to make Classic style testing easier.
    """
    def __init__(self, env=None,
                 docker_fingerprinter=None,
                 file_fingerprinter=None,
                 sha256_fingerprinter=None):
        self._env = env
        self._docker_fingerprinter = docker_fingerprinter
        self._file_fingerprinter = file_fingerprinter
        self._sha256_fingerprinter = sha256_fingerprinter

        if self._env is None:
            self._env = os.environ

        if self._docker_fingerprinter is None:
            self._docker_fingerprinter = DockerFingerprinter()

        if self._file_fingerprinter is None:
            self._file_fingerprinter = FileFingerprinter()

        if self._sha256_fingerprinter is None:
            self._sha256_fingerprinter = Sha256Fingerprinter()

    @property
    def env(self):
        return self._env

    @property
    def docker_fingerprinter(self):
        return self._docker_fingerprinter

    @property
    def file_fingerprinter(self):
        return self._file_fingerprinter

    @property
    def sha256_fingerprinter(self):
        return self._sha256_fingerprinter