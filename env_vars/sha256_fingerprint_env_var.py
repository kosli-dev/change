class Sha256FingerprintEnvVar:

    def __init__(self, command, protocol, sha_and_artifact_name):
        self.__command = command
        self.__protocol = protocol
        self.__sha_and_artifact_name = sha_and_artifact_name

    @property
    def artifact_name(self):
        return self.__command.sha256_fingerprinter.artifact_name(self.__sha_and_artifact_name)

    @property
    def artifact_basename(self):
        return self.__command.sha256_fingerprinter.artifact_basename(self.__sha_and_artifact_name)

    @property
    def sha(self):
        return self.__command.sha256_fingerprinter.sha(self.__protocol, self.__sha_and_artifact_name)
