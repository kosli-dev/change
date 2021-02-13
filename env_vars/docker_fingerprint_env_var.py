class DockerFingerprintEnvVar:

    def __init__(self, command, protocol, artifact_name):
        self.__command = command
        self.__protocol = protocol
        self.__artifact_name = artifact_name

    @property
    def artifact_name(self):
        return self.__command.docker_fingerprinter.artifact_name(self.__artifact_name)

    @property
    def artifact_basename(self):
        return self.__command.docker_fingerprinter.artifact_basename(self.__artifact_name)

    @property
    def sha(self):
        return self.__command.docker_fingerprinter.sha(self.__protocol, self.__artifact_name)

