class DockerFingerprintEnvVar:

    def __init__(self, command, protocol, artifact_name):
        self.__command = command
        self.__protocol = protocol
        self.__artifact_name = artifact_name

    @property
    def notes(self):
        return "\n".join([
            f'The string `{self.__protocol}` followed by the name+tag of the docker image to fingerprint.',
            'The docker socket must be volume-mounted.',
            'Example:',
            'docker run ... \\',
            f'    --env MERKELY_FINGERPRINT=”{self.__protocol}${{YOUR_DOCKER_IMAGE_AND_TAG}}" \\',
            '    --volume /var/run/docker.sock:/var/run/docker.sock \\',
            '    ...',
        ])

    @property
    def artifact_name(self):
        return self.__artifact_name

    @property
    def artifact_basename(self):
        return self.artifact_name

    @property
    def sha(self):
        return self.__command.docker_fingerprinter(self.__protocol, self.artifact_name)

