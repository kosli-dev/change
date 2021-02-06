import os
from .fingerprinter import Fingerprinter


class Context:
    """
    Holds (some) external dependencies to make Classic style testing easier.
    """
    def __init__(self, env=None, fingerprinter=None):
        if env is None:
            self._env = os.environ
        else:
            self._env = env
        if fingerprinter is None:
            self._fingerprinter = Fingerprinter()
        else:
            self._fingerprinter = fingerprinter

    @property
    def env(self):
        return self._env

    def fingerprint(self, command):
        return self._fingerprinter.fingerprint(command)

