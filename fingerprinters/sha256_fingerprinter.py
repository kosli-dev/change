from fingerprinters import Fingerprinter
from collections import namedtuple
import re

PROTOCOL = 'sha256://'

NOTES = " ".join([
    f"The string `{PROTOCOL}` followed by the artifact's 64 character sha256, ',"
    "then `/`, then it's non-empty name."
])

EXAMPLE = "\n".join([
    'docker run ... \\',
    f'    --env MERKELY_FINGERPRINT=”{PROTOCOL}${{YOUR_ARTIFACT_SHA256}}/${{YOUR_ARTIFACT_NAME}}” \\',
    '    ...',
])


class Sha256Fingerprinter(Fingerprinter):

    @property
    def notes(self):
        return NOTES

    @property
    def example(self):
        return EXAMPLE

    def handles_protocol(self, string):
        return string.startswith(PROTOCOL)

    def artifact_basename(self, string):
        return self.__validated(string).artifact_name

    def artifact_name(self, string):
        return self.__validated(string).artifact_name

    def sha(self, string):
        return self.__validated(string).sha

    __REGEX = re.compile(r'(?P<sha>[0-9a-f]{64})\/(?P<artifact_name>.+)')

    def __validated(self, string):
        assert self.handles_protocol(string)
        after_protocol = string[len(PROTOCOL):]
        match = self.__REGEX.match(after_protocol)
        if match is None:
            from commands import CommandError
            raise CommandError(f"Invalid {PROTOCOL} fingerprint: {after_protocol}")
        names = ('sha', 'artifact_name')
        args = (match.group('sha'), match.group('artifact_name'))
        return namedtuple('Both', names)(*args)
