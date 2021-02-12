class DockerFingerprintEnvVar:

    def __init__(self, command, protocol, artifact_name):
        self._command = command
        self._protocol = protocol
        self._artifact_name = artifact_name

    @property
    def notes(self):
        return "\n".join([
            'The string `docker://` followed by the name+tag of the docker image to fingerprint.',
            'The docker socket must be volume-mounted.',
            'Example:',
            'docker run ... \\',
            '    --env MERKELY_FINGERPRINT=”docker://${YOUR_DOCKER_IMAGE_AND_TAG}" \\',
            '    --volume /var/run/docker.sock:/var/run/docker.sock \\',
            '    ...',
        ])

    @property
    def artifact_name(self):
        return self._artifact_name

    @property
    def sha(self):
        return self._command.docker_fingerprinter(self._protocol, self.artifact_name)

