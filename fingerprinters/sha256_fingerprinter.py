from fingerprinters import Fingerprinter
from collections import namedtuple
import re

PROTOCOL = 'sha256://'


class Sha256Fingerprinter(Fingerprinter):

    @property
    def notes(self):
        return "\n".join([
            f"The string `{PROTOCOL}` followed by the artifact's 64 character sha256, then `/`, then it's non-empty name."
            'Example:',
            'docker run ... \\',
            f'    --env MERKELY_FINGERPRINT=”{PROTOCOL}${{YOUR_ARTIFACT_SHA256}}/${{YOUR_ARTIFACT_NAME}}” \\',
            '    ...',
        ])

    @property
    def protocol(self):
        return PROTOCOL

    def handles_protocol(self, s):
        return s.startswith(PROTOCOL)

    def artifact_name(self, sha_and_artifact_name):
        return self.__validated(sha_and_artifact_name).artifact_name

    def artifact_basename(self, sha_and_artifact_name):
        return self.artifact_name(sha_and_artifact_name)

    def sha(self, sha_and_artifact_name):
        return self.__validated(sha_and_artifact_name).sha

    __REGEX = re.compile(r'(?P<sha>[0-9a-f]{64})\/(?P<artifact_name>.+)')

    def __validated(self, sha_and_artifact_name):
        match = self.__REGEX.match(sha_and_artifact_name)
        if match is None:
            from commands import CommandError
            raise CommandError(f"Invalid {PROTOCOL} fingerprint: {sha_and_artifact_name}")
        names = ('sha', 'artifact_name')
        args = (match.group('sha'), match.group('artifact_name'))
        return namedtuple('Both', names)(*args)
