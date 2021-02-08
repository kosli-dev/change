from commands import CommandError
from env_vars import RequiredEnvVar

FILE_PROTOCOL = 'file://'
DOCKER_PROTOCOL = 'docker://'
SHA256_PROTOCOL = 'sha256://'

DESCRIPTION = "\n".join([
    '1. If prefixed by docker:// the name+tag of the docker image to fingerprint.',
    '   The docker socket must be volume-mounted.',
    '   Example:',
    '     --env MERKELY_FINGERPRINT=”docker://${YOUR_DOCKER_IMAGE_AND_TAG}"',
    '     --volume /var/run/docker.sock:/var/run/docker.sock',
    '',
    '2. If prefixed by file:// the full path of the file to fingerprint.',
    '   The full path must be volume-mounted.',
    '   Example:',
    '     --env MERKELY_FINGERPRINT=”file://${YOUR_FILE_PATH}',
    '     --volume=${YOUR_FILE_PATH}:${YOUR_FILE_PATH}',
    '',
    "3. If prefixed by sha256:// the artifact's sha256 digest."
    '   The name of the artifact must be provided in MERKELY_DISPLAY_NAME',
    '   Example:',
    '     --env MERKELY_FINGERPRINT=”sha256://${YOUR_ARTIFACT_SHA256}”',
    '     --env MERKELY_DISPLAY_NAME=”${YOUR_ARTIFACT_NAME}”'
])


class FingerprintEnvVar(RequiredEnvVar):

    def __init__(self, command):
        super().__init__(command.env, "MERKELY_FINGERPRINT", DESCRIPTION)
        self._command = command

    @property
    def protocol(self):
        if self.value.startswith(FILE_PROTOCOL):
            return FILE_PROTOCOL
        elif self.value.startswith(DOCKER_PROTOCOL):
            return DOCKER_PROTOCOL
        elif self.value.startswith(SHA256_PROTOCOL):
            return SHA256_PROTOCOL
        else:
            raise self.unknown_protocol_error()

    @property
    def artifact_name(self):
        return self.value[len(self.protocol):]

    @property
    def sha(self):
        if self.protocol == FILE_PROTOCOL:
            return self._command.file_fingerprinter(self.protocol, self.artifact_name)
        elif self.protocol == DOCKER_PROTOCOL:
            return self._command.docker_fingerprinter(self.protocol, self.artifact_name)
        elif self.protocol == SHA256_PROTOCOL:
            return self.artifact_name
        else:
            raise self.unknown_protocol_error()

    def unknown_protocol_error(self):
        return CommandError(f"Unknown protocol: {self.value}")
