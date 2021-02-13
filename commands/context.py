import os
from commands import CommandError
from fingerprinters import *


class Context:
    """
    Holds (some) external dependencies to make Classic style testing easier.
    """
    def __init__(self, env=None,
                 docker_fingerprinter=None,
                 file_fingerprinter=None,
                 sha256_fingerprinter=None):
        self.__env = env
        self.__docker_fingerprinter = docker_fingerprinter
        self.__file_fingerprinter = file_fingerprinter
        self.__sha256_fingerprinter = sha256_fingerprinter

        if self.__env is None:
            self.__env = os.environ

        if self.__docker_fingerprinter is None:
            self.__docker_fingerprinter = DockerFingerprinter()

        if self.__file_fingerprinter is None:
            self.__file_fingerprinter = FileFingerprinter()

        if self.__sha256_fingerprinter is None:
            self.__sha256_fingerprinter = Sha256Fingerprinter()

    @property
    def env(self):
        return self.__env

    def fingerprinter_for(self, string):
        d = self.__docker_fingerprinter
        f = self.__file_fingerprinter
        s = self.__sha256_fingerprinter
        if d.handles_protocol(string):
            return d
        elif f.handles_protocol(string):
            return f
        elif s.handles_protocol(string):
            return s
        else:
            raise CommandError(f"Unknown protocol: {string}")

