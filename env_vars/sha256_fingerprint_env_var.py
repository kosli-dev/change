from collections import namedtuple
from commands import CommandError
import re


class Sha256FingerprintEnvVar:

    def __init__(self, _command, protocol, sha_and_artifact_name):
        self.__protocol = protocol
        self.__sha_and_artifact_name = sha_and_artifact_name

    @property
    def artifact_name(self):
        return self.__validated.artifact_name

    @property
    def artifact_basename(self):
        return self.artifact_name

    @property
    def sha(self):
        return self.__validated.sha

    __REGEX = re.compile(r'(?P<sha>[0-9a-f]{64})\/(?P<artifact_name>.+)')

    @property
    def __validated(self):
        string = self.__sha_and_artifact_name
        match = self.__REGEX.match(string)
        if match is None:
            raise CommandError(f"Invalid {self.__protocol} fingerprint: {string}")
        names = ('sha', 'artifact_name')
        args = (match.group('sha'), match.group('artifact_name'))
        return namedtuple('Both', names)(*args)
