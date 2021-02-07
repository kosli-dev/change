import os
from .docker_fingerprinter import DockerFingerprinter
from .file_fingerprinter import FileFingerprinter


class Context:
    """
    Holds (some) external dependencies to make Classic style testing easier.
    """
    def __init__(self, env=None, docker_fingerprinter=None, file_fingerprinter=None):
        self._env = env
        self._docker_fingerprinter = docker_fingerprinter
        self._file_fingerprinter = file_fingerprinter

        if self._env is None:
            self._env = os.environ

        if self._docker_fingerprinter is None:
            self._docker_fingerprinter = DockerFingerprinter()

        if self._file_fingerprinter is None:
            self._file_fingerprinter = FileFingerprinter()

    @property
    def env(self):
        return self._env

    @property
    def docker_fingerprinter(self):
        return self._docker_fingerprinter

    @property
    def file_fingerprinter(self):
        return self._file_fingerprinter

