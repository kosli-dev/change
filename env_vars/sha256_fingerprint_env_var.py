from collections import namedtuple
from commands import CommandError
import re


class Sha256FingerprintEnvVar:

    def __init__(self, _command, protocol, sha_and_artifact_name):
        self._protocol = protocol
        self._sha_and_artifact_name = sha_and_artifact_name

    @property
    def notes(self):
        return "\n".join([
            "The string `sha256://` followed by the artifact's 64 character sha256, then `/`, then it's non-empty name."
            'Example:',
            'docker run ... \\',
            '    --env MERKELY_FINGERPRINT=”sha256://${YOUR_ARTIFACT_SHA256}/${YOUR_ARTIFACT_NAME}” \\',
            '    ...',
        ])

    @property
    def artifact_name(self):
        return self._validated.artifact_name

    @property
    def sha(self):
        return self._validated.sha

    _REGEX = re.compile(r'(?P<sha>[0-9a-f]{64})\/(?P<artifact_name>.+)')

    @property
    def _validated(self):
        string = self._sha_and_artifact_name
        match = self._REGEX.match(string)
        if match is None:
            raise CommandError(f"Invalid {self._protocol} fingerprint: {string}")
        names = ('sha', 'artifact_name')
        args = (match.group('sha'), match.group('artifact_name'))
        return namedtuple('Both', names)(*args)
